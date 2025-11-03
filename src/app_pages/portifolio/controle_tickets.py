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
from datetime import datetime
from tools.api_data import buscar_dados_random_user, processar_dados_random_user
from mockup_data.faker_data_generation import gerar_dados_tickets

# region Config Página
# Nesta seção é definido o título da página, o layout e os itens de menu - itens para
# explicar o projeto, com o problema e a solução adotada.
st.set_page_config(
    page_title="Controle de tickets",
    layout="wide",
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
    return gerar_dados_tickets(qtd=qtd, df_analistas=df_analistas)


# endregion

# region Random Qtd
random_qtd_analistas = random.randint(5, 25)
random_qtd_tickets = random.randint(5, 200)
# endregion

# region Session State
if "analistas" not in ss:
    ss.analistas = gerar_dados_analistas(qtd=random_qtd_analistas)
    ss.df_analistas = (
        processar_dados_random_user(ss.analistas)
        .with_columns((pl.col("Nome") + " " + pl.col("Sobrenome")).alias("Analista"))
        .select(["Foto", "Analista", "Email Empresarial", "Telefone"])
    )

if "tickets" not in ss:
    ss.tickets = dados_tickets(qtd=random_qtd_tickets, df_analistas=ss.df_analistas)
    ss.df_tickets = pl.DataFrame(ss.tickets)

# DFs
df_analistas: pl.DataFrame = ss.df_analistas
df_tickets: pl.DataFrame = ss.df_tickets

# endregion

# region Sidebar
# Botão - Gerar Novos Dados
with st.sidebar:
    if st.button(label="Gerar Novos Dados", width="stretch"):
        ss.analistas = gerar_dados_analistas(qtd=random_qtd_analistas)
        ss.df_analistas = (
            processar_dados_random_user(ss.analistas)
            .with_columns(
                (pl.col("Nome") + " " + pl.col("Sobrenome")).alias("Analista")
            )
            .select(["Foto", "Analista", "Email Empresarial", "Telefone"])
        )

        ss.tickets = dados_tickets(qtd=random_qtd_tickets, df_analistas=ss.df_analistas)
        ss.df_tickets = pl.DataFrame(ss.tickets)
        st.rerun()

# endregion

# region App
st.title(
    "Controle de Tickets",
)

with st.expander(label="Sobre esta solução", expanded=False):
    col1, col2, col3 = st.columns(spec=3, gap="small")
    with col1:
        st.markdown(
            """
            ##### **O PROBLEMA**:

            A geração do painel de acompanhamento dos tickets por analista era um 
            processo moroso e manual, sendo realizado, no mínimo, duas vezes por dia 
            para ter a visão gerencial de todos os tickets abertos, pendentes e em 
            atendimento por mais de 15 dias.
            """
        )

    with col2:
        st.markdown(
            """
            ##### **A SOLUÇÃO**:

            Criamos um painel automatizado onde não é mais necessário a atualização 
            manual. O painel acessa a API da plataforma e retorna os dados necessários, 
            já tratados e atualizados.

            Além disso, como melhoria adicional, criamos uma sessão onde o analista pode
            consultar seus tickets. Nesta sessão, ele poderá até mesmo filtrar os dados 
            para visualizar somente os tickets abertos a mais de 15 dias em atendimento.
            """
        )

    with col3:
        st.markdown(
            """
            ##### **OS IMPACTOS**:
            1) Diminuição de atividades que não geram impacto real;
            2) Informações de tickets atualizadas sistemicamente quando necessário;
            3) A melhoria adicional possibilita que o analista tenha de forma
            tempestiva os tickes que precisam ser priorizados (mais de 15 dias em 
            atendimento);    
            """
        )

    st.write("---")

    st.markdown(
        """
        ##### **PRÓXIMOS PASSOS**:
        Para evolução e melhoria contínua deste painel, seguem sugestões:
        1) Inclusão de outros KPIs relevantes para a área e objetivo do painel;
        2) Inclusão de filtros para visualização de todos os tickets;
        3) Possibilidade da exportação dos dados para arquivos Excel;
        """
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
    with st.sidebar:
        relacao_analistas: pl.DataFrame = ss.df_analistas
        analista_selecionado: list[str] = st.multiselect(
            label="Analista",
            width=400,
            options=relacao_analistas.select(pl.col("Analista"))
            .unique()
            .sort("Analista")
            .to_series()
            .to_list(),
            placeholder="Selecione pelo nome do analista",
        )

    if not analista_selecionado:
        st.warning(
            """
            Nenhum analista selecionado.
            
            Selecione um analista na barra lateral para visualizar sua sessão.
            """
        )

    for analista in analista_selecionado:
        dados_analista = ss.df_analistas.filter(pl.col("Analista") == analista)
        tickets_analista = df_tickets.filter(pl.col("Analista") == analista)

        col1, col2, col3 = st.columns(
            spec=[0.1, 0.3, 0.6],
            vertical_alignment="bottom",
        )

        with col1:
            st.image(
                dados_analista["Foto"][0],
                width=180,
            )

        with col2:
            st.title(f"{analista}")
            st.write(f"Tel Comercial: {dados_analista["Telefone"][0]}")
            st.write(f"E-mail Comercial: {dados_analista["Email Empresarial"][0]}")

        with col3:
            col1, col2, col3, col4 = st.columns(spec=4, gap="medium")
            with col1:
                base = alt.Chart(tickets_analista).encode(
                    y=alt.Y("Status Ticket:N", title=None),
                    x=alt.X("count(Status Ticket):Q", title=None),
                    color=alt.Color(
                        "Status Ticket:N",
                        legend=None,
                    ).scale(scheme="lightgreyred"),
                )

                bars = base.mark_bar()

                text = base.mark_text(
                    align="left",
                    dx=3,  # Offset from the end of bars
                    size=15,
                    color="white",
                    fontWeight="bold",
                ).encode(text="count(*):Q")

                chart = alt.layer(bars, text)

                st.altair_chart(chart, use_container_width=True)

            with col2:
                st.metric(
                    label="Tickets em Atendimento",
                    value=f"{tickets_analista.filter(
                            (pl.col("Status Ticket").is_in(["Aberto", "Pendente"]))
                ).count()[0, 0]:,}",
                    border=False,
                    height="content",
                    help="""
                        Tickets em atendimento (abertos ou pendentes).
                        """,
                )

            with col3:
                st.metric(
                    label="Qtd tickets > 15 dias",
                    value=f"{tickets_analista.filter(
                        (pl.col("Status Ticket").is_in(["Aberto", "Pendente"])) &
                        ((datetime.now() - pl.col("Data Criação Ticket"))
                        .dt.total_days() > 15)
                    ).count()[0, 0]:,}",
                    border=False,
                    height="content",
                    help="""
                        Tickets em atendimento (abertos ou pendentes) com data de 
                        criação maior que 15 dias.
                        """,
                )

            with col4:
                st.write("Opções de visualização")

                somente_tkt_15_dias = st.toggle(
                    label="Mais de 15 dias",
                    value=False,
                    key=f"toggle15dias{analista}",
                )
                if somente_tkt_15_dias:
                    tickets_analista = tickets_analista.filter(
                        (pl.col("Status Ticket").is_in(["Aberto", "Pendente"]))
                        & (
                            (
                                datetime.now() - pl.col("Data Criação Ticket")
                            ).dt.total_days()
                            > 15
                        )
                    )

                somente_tkt_atendimento = st.toggle(
                    label="Em atendimento",
                    value=False,
                    key=f"toggleematendimento{analista}",
                )
                if somente_tkt_atendimento:
                    tickets_analista = tickets_analista.filter(
                        (pl.col("Status Ticket").is_in(["Aberto", "Pendente"]))
                    )

        with st.expander(label="Relação de Tickets", expanded=False):
            st.dataframe(data=tickets_analista, width="stretch")
        st.write("---")
