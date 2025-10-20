"""
Projeto: Extrato de Serviços
Objetivo: Criar um painel para exibir o serviços prestados por projeto, para que seja
possível analisar, validar e exportar os dados em excel para envio ao cliente, se
necessário.

Este painel padroniza o processo da extração dos dados já tratados, facilita a análise
pelo usuário, e agiliza o atendimento ao cliente caso este precise de mais informações
sobre os serviços prestados.
"""

import altair as alt
import streamlit as st
import polars as pl
import random

from mockup_data.faker_data_generation import (
    gerar_dados_projeto,
    gerar_servicos_projeto,
)
from tools.data_tools import salvar_xlsx
from streamlit import session_state as ss
from datetime import datetime, timedelta

# region Config Página
# Nesta seção é definido o título da página, o layout e os itens de menu - itens para
# explicar o projeto, com o problema e a solução adotada.
st.set_page_config(
    page_title="Extrato de Serviços",
    layout="wide",
    menu_items={
        "About": """
    PROBLEMA:

    Os analistas recebiam diversas solicitações de clientes para o envio
    de mais informações sobre os serviços prestados contendo a composição do que 
    foi cobrado. Os analistas precisavam encontrar estes dados no sistema, extrair 
    relatórios, tratar, recalcular e confirmar se estava tudo correto, para então enviar
    ao cliente.

    SOLUÇÃO:
    
    Padronizamos o processo de análise e extração por meio de um painel que
    permite a visualização dos dados, a exportação em excel já formatado e recalculado,
    facilitando e agilizando o atendimento ao cliente. Neste painel, as informações
    entre as diferentes tabelas (tabela de projetos e tabela de serviços) já estão
    relacionadas, e o usuário pode filtrar por projeto, cliente, data, etc para extrair
    apenas os dados que precisa enviar.
    """,
    },
)
# endregion


# region Gerar Dados
def gerar_dados() -> list[dict]:
    """
    Função para gerar dados para o extrato de serviços por projeto.
    Retorna uma lista de dicionários com os dados gerados.

    Returns:
        list[dict]:
        Lista de dicionários com os dados gerados para projetos e serviços.
    """

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
    if st.button(label="Gerar Novos Dados", width="stretch"):
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
    responsavel_servico_selecionado: str = st.multiselect(
        label="Responsável pelo Serviço",
        options=df_servicos_taxahora.select(pl.col("Responsável pelo Serviço"))
        .unique()
        .sort("Responsável pelo Serviço")
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

    if responsavel_servico_selecionado:
        df_filtrada = df_filtrada.filter(
            pl.col("Responsável pelo Serviço").is_in(responsavel_servico_selecionado)
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

    st.download_button(
        label="Exportar para Excel",
        data=salvar_xlsx(df_filtrada.collect()),
        file_name="extrato_servicos.xlsx",
    )

with tab2:
    st.write("### Visualizações Gráficas")

    # Dashboard - Custo Total
    with st.expander(label="Custo Total", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("#### Por Período")
            df_custo_por_periodo = (
                df_servicos_filtrados_taxahora.sort("Data Serviço")
                .group_by_dynamic(
                    "Data Serviço",
                    every="1mo",
                )
                .agg(
                    pl.col("Custo Serviço").sum().alias("Custo Serviço"),
                )
            )

            fig = (
                alt.Chart(
                    df_custo_por_periodo.sort(
                        "Data Serviço",
                        descending=True,
                    ),
                    title="Evolução do custo total de serviços (em R$)",
                )
                .mark_line(point=True)
                .encode(
                    x=alt.X(
                        "Data Serviço:T",
                        title=None,
                        axis=alt.Axis(format="%m/%Y"),
                    ),
                    y=alt.Y(
                        "sum(Custo Serviço):Q",
                        title=None,
                        axis=alt.Axis(format=",.2f"),
                    ),
                    color=alt.Color("sum(Custo Serviço):Q", legend=None).scale(
                        scheme="greens"
                    ),
                    tooltip=[
                        alt.Tooltip("Data Serviço:T", title="Período", format="%m/%Y"),
                        alt.Tooltip(
                            "sum(Custo Serviço):Q", title="Custo Total", format=",.2f"
                        ),
                    ],
                )
                .configure_point(size=50)
            )
            st.altair_chart(fig, use_container_width=True)

        with col2:
            st.write("#### Por Cliente (TOP 10)")
            df_custo_por_cliente = df_servicos_filtrados_taxahora.group_by(
                [
                    "Nome Cliente",
                    "ID Cliente",
                    "CNPJ Cliente",
                    "Projeto Vinculado",
                ]
            ).agg(pl.col("Custo Serviço").sum())

            fig = (
                alt.Chart(
                    df_custo_por_cliente.sort("Custo Serviço", descending=True).head(
                        10
                    ),
                    title="Clientes com maior valor de custo total de serviços (em R$)",
                )
                .mark_bar()
                .encode(
                    x=alt.X("Nome Cliente:N", sort="-y", title=None),
                    y=alt.Y("Custo Serviço:Q", title=None),
                    color=alt.Color("Custo Serviço:Q").scale(scheme="greens"),
                )
            )
            st.altair_chart(fig, use_container_width=True)

    # Dashboard - Projetos
    with st.expander(label="Projetos", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("#### Por Período")
            df_projetos_por_periodo = (
                df_servicos_filtrados_taxahora.sort("Data Criação Projeto")
                .group_by_dynamic(
                    "Data Criação Projeto",
                    every="1mo",
                )
                .agg(
                    pl.col("Projeto Vinculado").unique().count().alias("Quantidade"),
                )
            )

            fig = (
                alt.Chart(
                    df_projetos_por_periodo.sort(
                        "Data Criação Projeto", descending=True
                    ),
                    title="Evolução da quantidade de projetos (em unidades)",
                )
                .mark_line(point=True)
                .encode(
                    x=alt.X(
                        "Data Criação Projeto:T",
                        title=None,
                        axis=alt.Axis(format="%m/%Y"),
                    ),
                    y=alt.Y(
                        "sum(Quantidade):Q",
                        title=None,
                        axis=alt.Axis(format=",.2f"),
                    ),
                    color=alt.Color("sum(Quantidade):Q", legend=None).scale(
                        scheme="blues"
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "Data Data Criação Projeto:T",
                            title="Período",
                            format="%m/%Y",
                        ),
                        alt.Tooltip(
                            "sum(Quantidade):Q",
                            title="Quantidade de Projetos",
                            format=",.2f",
                        ),
                    ],
                )
                .configure_point(size=50)
            )
            st.altair_chart(fig, use_container_width=True)

        with col2:
            st.write("#### Por Valor (TOP 10)")
            df_projetos_por_valor = df_servicos_filtrados_taxahora.group_by(
                [
                    "Projeto Vinculado",
                    "Nome Projeto",
                    "Nome Cliente",
                    "ID Cliente",
                    "CNPJ Cliente",
                ]
            ).agg(pl.col("Custo Serviço").sum())

            fig = (
                alt.Chart(
                    df_projetos_por_valor.sort("Custo Serviço", descending=True).head(
                        10
                    ),
                    title="Projetos com maior valor de custo total de serviços (em R$)",
                )
                .mark_bar()
                .encode(
                    x=alt.X("Projeto Vinculado:N", sort="-y", title=None),
                    y=alt.Y("Custo Serviço:Q", title=None),
                    color=alt.Color("Custo Serviço:Q").scale(scheme="blues"),
                    tooltip=[
                        alt.Tooltip(
                            "Projeto Vinculado:N",
                            title="Código do Projeto",
                        ),
                        alt.Tooltip(
                            "Nome Projeto:N",
                            title="Nome do Projeto",
                        ),
                        alt.Tooltip(
                            "Nome Cliente:N",
                            title="Nome do Cliente",
                        ),
                        alt.Tooltip(
                            "ID Cliente:N",
                            title="Código do Cliente",
                        ),
                        alt.Tooltip(
                            "CNPJ Cliente:N",
                            title="CNPJ do Cliente",
                        ),
                        alt.Tooltip(
                            "Custo Serviço:Q", title="Custo Total", format=",.2f"
                        ),
                    ],
                )
            )
            st.altair_chart(fig, use_container_width=True)


# endregion
