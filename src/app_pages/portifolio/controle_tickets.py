"""
Projeto: Painel Gerencial de Controle de Tickets
Objetivo: Criar um painel para a gerencia e supervisão para acompanhar o andamento
dos tickets por analista.

Este painel acessa a API da plataforme de controle de tickets, retorna os dados
necessários apresenta as principais informações para facilitar o gerenciamento e
acompanhamento dos tickets em andamento.

Visto que o painel está ligado via API, as informações sempre estarão atualizadas.
"""

import altair as alt
import streamlit as st
import polars as pl
import random

from streamlit import session_state as ss
from tools.api_data import buscar_dados_random_user, processar_dados_random_user
from mockup_data.faker_data_generation import gerar_dados_tickets

# region Config Página
# Nesta seção é definido o título da página, o layout e os itens de menu - itens para
# explicar o projeto, com o problema e a solução adotada.
st.set_page_config(
    page_title="Controle de tickets",
    layout="wide",
    menu_items={
        "About": """
    PROBLEMA:

    Diaramente o time recebe tickets em uma plataforma específica para atenderem 
    solicitações de clientes ou de áreas internas. Para que a gerencia possa controlar
    o andamento dos tickets, era necessário extrair os relatórios da plataforma, 
    tratá-los manualmente e atualizar os dados na ferramenta de BI, o que consumia
    muito tempo além de não ter as informações atualizadas ao longo do dia 
    (era necessário extrair os relatorios novamente e refazer o processo).


    SOLUÇÃO:

    Criamos um painel que acessa a API da plataforma de tickets, retorna os dados 
    necessários já tratados e realiza atualização automática do painel, e desta forma
    eliminamos o retrabalho para apresentar as informações atualizadas.
    Também foi criado como melhoria adicional uma sessão para que cada analista possa
    consultar seus tickets. O analista pode ir até a aba "Tickets por Analista"
    selecionar seu nome e assim o painel com os dados do tickets que ele está 
    responsável será gerada.
    """,
    },
)
# endregion


# region Gerar Dados
# Analistas - RandomUser.me
def gerar_dados_analistas(qtd: int = 10) -> list[dict]:
    """
    Função para gerar dados para os analistas.
    Retorna uma lista de dicionários com os dados gerados.

    Args:
        qtd (int, optional):
        Quantidade de analistas a serem gerados. Padrão é 10.

    Returns:
        list[dict]:
        Lista de dicionários com os dados gerados para analistas.
    """
    return buscar_dados_random_user(qtd)


# Tickets - Faker
def dados_tickets(
    qtd: int = 10, df_analistas: pl.DataFrame = pl.DataFrame()
) -> pl.DataFrame:
    """
    Função para gerar dados para os tickets.
    Retorna uma lista de dicionários com os dados gerados.

    Returns:
        list[dict]:
        Lista de dicionários com os dados gerados para tickets.
    """
    return gerar_dados_tickets(qtd=random.randint(5, 15), df_analistas=df_analistas)


# endregion

# region Session State
if "analistas" not in ss:
    ss.analistas = gerar_dados_analistas(qtd=random.randint(10, 25))
    ss.df_analistas = (
        processar_dados_random_user(ss.analistas)
        .with_columns((pl.col("Nome") + " " + pl.col("Sobrenome")).alias("Analista"))
        .select(["Foto", "Analista", "Email Empresarial", "Telefone"])
    )

if "tickets" not in ss:
    ss.tickets = dados_tickets(
        qtd=random.randint(10, 150), df_analistas=ss.df_analistas
    )
    ss.df_tickets = pl.DataFrame(ss.tickets)

# DFs
df_analistas: pl.DataFrame = ss.df_analistas
df_tickets: pl.DataFrame = ss.df_tickets

# endregion

# region Sidebar
# Botão - Gerar Novos Dados
with st.sidebar:
    if st.button(label="Gerar Novos Dados", width="stretch"):
        ss.analistas = gerar_dados_analistas(qtd=random.randint(10, 25))
        ss.df_analistas = (
            processar_dados_random_user(ss.analistas)
            .with_columns(
                (pl.col("Nome") + " " + pl.col("Sobrenome")).alias("Analista")
            )
            .select(["Foto", "Analista", "Email Empresarial", "Telefone"])
        )

        ss.tickets = dados_tickets(
            qtd=random.randint(10, 250), df_analistas=ss.df_analistas
        )
        ss.df_tickets = pl.DataFrame(ss.tickets)
        st.rerun()

# endregion

# region App
st.title(
    "Controle de Tickets (Página em Desenvolvimento)",
)
st.write(
    "*Para mais informações sobre este projeto, acesse o menu no canto superior "
    "direito (os três pontos), e clique em 'About'.*"
)
st.write(
    "*Todas as informações são fictícias, geradas aleatoriamente utilizando a "
    "API do site randomuser.me e biblioteca Faker para simular situações reais.*"
)
st.write("---")

tabs = st.tabs(
    [
        "Resumo",
        "Relação de Tickets",
        "Tickets por Analista",
    ]
)

with tabs[0]:
    st.write("### Resumo")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Tickets Abertos",
            value=f"{len(df_tickets.filter(pl.col('Status Ticket') == 'Aberto')):,}",
            border=True,
        )

    with col2:
        st.metric(
            label="Tickets Pendentes",
            value=f"{len(df_tickets.filter(pl.col('Status Ticket') == 'Pendente')):,}",
            border=True,
        )

    with col3:
        st.metric(
            label="Tickets Concluídos",
            value=f"{len(df_tickets.filter(pl.col('Status Ticket') == 'Concluído')):,}",
            border=True,
        )

    st.write("### Comparativo Mes a Mes")

    fig = (
        alt.Chart(
            df_tickets,
            title="Tickets por período, considerando a data de criação",
        )
        .mark_bar()
        .encode(
            x=alt.X(
                "Data Criação Ticket:N",
                timeUnit="yearmonth",
                axis=alt.Axis(format="%m/%Y"),
                title="Período",
            ),
            xOffset="Status Ticket",
            y=alt.Y(
                field="Status Ticket",
                aggregate="count",
                title="Quantidade",
            ),
            color=alt.Color("Status Ticket", legend={"orient": "top"}).scale(
                scheme="lightgreyred"
            ),
            text="count(*):Q",
        )
    )

    fig_labels = fig + fig.mark_text(
        align="center", dy=-10, size=15, blend="difference", fontWeight="bold"
    )

    st.altair_chart(fig_labels, use_container_width=True)

with tabs[1]:
    st.write("### Relação de Tickets")
    st.dataframe(data=df_tickets, width="stretch")

with tabs[2]:
    st.write("### Tickets por Analista")

# endregion
