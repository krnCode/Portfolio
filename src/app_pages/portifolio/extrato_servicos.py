"""
Projeto: Extrato de Serviços
Objetivo: Criar um painel para exibir o serviços prestados por projeto, para que seja
possível analisar, validar e exportar os dados em excel para envio ao cliente, se
necessário.

Este painel padroniza o processo da extração dos dados já tratados, facilita a análise
pelo usuário, e agiliza o atendimento ao cliente caso este precise de mais informações
sobre os serviços prestados.
"""

import streamlit as st
import polars as pl
import random

from mockup_data.faker_data_generation import (
    gerar_dados_projeto,
    gerar_servicos_projeto,
)
from streamlit import session_state as ss
from datetime import datetime, timedelta

# region Conig Página
# Nesta seção é definido o título da página, o layout e os itens de menu - itens para
# explicar o projeto, com o problema e a solução adotada.
st.set_page_config(
    page_title="Extrato de Serviços",
    layout="wide",
    menu_items={
        "About": """
    PROBLEMA:
    Os analistas recebiam diversas solicitações de clientes para o envio
    de mais informações sobre os serviços prestados para entender a composição do que 
    foi cobrado. Os analistas precisavam encontrar as informações no sistema, extrair 
    relatórios, tratar, recalcular e confirmar se estava tudo correto, para então enviar
    ao cliente.

    SOLUÇÃO:
    Padronizamos o processo de análise e extração por meio de um painel que
    permite a visualização dos dados, a exportação em excel já formatado e recalculado,
    facilitando e agilizando o atendimento ao cliente. Neste painel, as informações
    entre as diferentes tabelas (tabela de projetos e tabela de serviços) já estão
    relacionadas, e o usuário pode filtrar por projeto, cliente, data, etc.
    """,
    },
)
# endregion


# region Gerar Dados
def gerar_dados():

    dados_projeto: list[dict] = gerar_dados_projeto(
        qtd_itens=random.randint(50, 200),
        qtd_projetos=random.randint(10, 400),
        qtd_clientes=random.randint(10, 500),
    )

    servicos_projeto: list[dict] = [
        gerar_servicos_projeto(projeto=projeto, qtd_servicos=random.randint(50, 500))
        for projeto in dados_projeto
    ]

    return dados_projeto, servicos_projeto


if "dados_projeto" not in ss or "servicos_projeto" not in ss:
    ss.dados_projeto, ss.servicos_projeto = gerar_dados()

with st.sidebar:
    if st.button("Gerar Novos Dados"):
        ss.dados_projeto, ss.servicos_projeto = gerar_dados()
        st.rerun()
# endregion

# region Transformar Dados
df_projetos: pl.LazyFrame = pl.LazyFrame(ss.dados_projeto)
df_servicos: pl.LazyFrame = pl.LazyFrame(ss.servicos_projeto)

df_servicos_taxahora: pl.LazyFrame = (
    df_servicos.join(
        other=df_projetos,
        left_on="Projeto Vinculado",
        right_on="ID Projeto",
        how="inner",
    )
    .with_columns(
        (pl.col("QTD Horas") * pl.col("Taxa/Hora Contratada")).alias("Custo Serviço")
    )
    .sort(
        by=["Projeto Vinculado", "Data Serviço"],
        descending=[False, False],
    )
)
# endregion

# region Filtros
with st.sidebar:
    st.write("### Filtros")

    col1, col2 = st.columns(2)
    with col1:
        data_inicial: datetime = st.date_input(
            label="Data Inicial",
            value=datetime.today() - timedelta(days=3650),
            format="DD/MM/YYYY",
        )
    with col2:
        data_final: datetime = st.date_input(
            label="Data Final",
            value=datetime.today(),
            format="DD/MM/YYYY",
        )

    cod_projeto_selecionado: int = st.multiselect(
        label="Código do Projeto",
        options=df_servicos_taxahora.select(pl.col("Projeto Vinculado"))
        .unique()
        .sort("Projeto Vinculado")
        .collect()
        .to_series()
        .to_list(),
        placeholder="Selecione pelo código do projeto",
    )
    projeto_selecionado: str = st.multiselect(
        label="Nome do Projeto",
        options=df_servicos_taxahora.select(pl.col("Nome Projeto"))
        .unique()
        .sort("Nome Projeto")
        .collect()
        .to_series()
        .to_list(),
        placeholder="Selecione pelo nome do projeto",
    )
    cod_servico_selecionado: int = st.multiselect(
        label="Código do Serviço",
        options=df_servicos_taxahora.select(pl.col("ID Serviço"))
        .unique()
        .sort("ID Serviço")
        .collect()
        .to_series()
        .to_list(),
        placeholder="Selecione pelo código do serviço",
    )
    servico_selecionado: str = st.multiselect(
        label="Descrição Serviço",
        options=df_servicos_taxahora.select(pl.col("Descrição Serviço"))
        .unique()
        .sort("Descrição Serviço")
        .collect()
        .to_series()
        .to_list(),
        placeholder="Selecione pelo nome do serviço",
    )
    cod_cliente_selecionado: int = st.multiselect(
        label="Código do Cliente",
        options=df_servicos_taxahora.select(pl.col("ID Cliente"))
        .unique()
        .sort("ID Cliente")
        .collect()
        .to_series()
        .to_list(),
        placeholder="Selecione pelo código do cliente",
    )
    cliente_selecionado: str = st.multiselect(
        label="Nome do Cliente",
        options=df_servicos_taxahora.select(pl.col("Nome Cliente"))
        .unique()
        .sort("Nome Cliente")
        .collect()
        .to_series()
        .to_list(),
        placeholder="Selecione pelo nome do cliente",
    )

    # Aplicar filtros
    df_filtrada: pl.LazyFrame = df_servicos_taxahora.filter(
        pl.col("Data Serviço").is_between(data_inicial, data_final)
    )

    if cod_projeto_selecionado:
        df_filtrada = df_filtrada.filter(
            pl.col("Projeto Vinculado").is_in(cod_projeto_selecionado)
        )
    if projeto_selecionado:
        df_filtrada = df_filtrada.filter(
            pl.col("Nome Projeto").is_in(projeto_selecionado)
        )

    if cod_cliente_selecionado:
        df_filtrada = df_filtrada.filter(
            pl.col("ID Cliente").is_in(cod_cliente_selecionado)
        )
    if cliente_selecionado:
        df_filtrada = df_filtrada.filter(
            pl.col("Nome Cliente").is_in(cliente_selecionado)
        )

    if cod_servico_selecionado:
        df_filtrada = df_filtrada.filter(
            pl.col("ID Serviço").is_in(cod_servico_selecionado)
        )
    if servico_selecionado:
        df_filtrada = df_filtrada.filter(
            pl.col("Descrição Serviço").is_in(servico_selecionado)
        )

    df_servicos_filtrados_taxahora: pl.LazyFrame = df_filtrada.collect()

# endregion


# region App
st.title("Extrato de Serviços")
st.write(
    "*Para mais informações sobre este projeto, acesse o menu no canto superior "
    "direito (os três pontos), e clique em 'About'.*"
)
st.write(
    "*Todas as informações são fictícias, geradas aleatoriamente utilizando a "
    "biblioteca Faker  para simular situações reais.*"
)
st.write("---")

st.write("### Resumo")
col1, col2, col3 = st.columns(3)

with col1:
    total_servicos: float = df_filtrada.select(pl.col("Custo Serviço").sum()).collect()[
        0, 0
    ]
    st.metric(
        label="Valor Total dos Serviços", value=f"R$ {total_servicos:,.2f}", border=True
    )

with col2:
    total_horas: int = df_filtrada.select(pl.col("QTD Horas").sum()).collect()[0, 0]
    st.metric(
        label="Total de Horas",
        value=f"{total_horas:,.0f}h",
        border=True,
    )

with col3:
    qtd_servicos: int = df_filtrada.select(pl.len()).collect()[0, 0]
    st.metric(
        label="Quantidade de Serviços",
        value=f"{qtd_servicos:,}",
        border=True,
    )

tab1, tab2 = st.tabs(tabs=["Relação de Serviços", "Visualizações Gráficas"])

with tab1:
    st.write("### Relação de Serviços")
    st.dataframe(df_filtrada.collect(), width="stretch")
# endregion
