"""
Projeto: Painel Gerencial de Controle de Tickets
Objetivo: Criar um painel para a gerencia e supervisão para acompanhar o andamento
dos tickets por analista.

Este painel acessa a API da plataforme de controle de tickets, retorna os dados
necessários apresenta as principais informações para facilitar o gerenciamento e
acompanhamento dos tickets em andamento.

Visto que o painel está ligado via API, as informações sempre estarão atualizadas.
"""

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
    Também foi criado uma sessão para cada analista poder consultar o status de seus
    tickets como melhoria. O analista pode ir até a aba que tem seu nome e visualizar
    as informações dos tickets que ele está responsável.
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


if "analistas" not in ss:
    ss.analistas = gerar_dados_analistas(qtd=25)


# def dados_tickets(qtd: int = 10, df: pl.DataFrame = pl.DataFrame()) -> list[dict]:
#     """
#     Gera dados sintéticos com a quantidade de itens informada, sendo o padrão 10 itens.

#     Args:
#         qtd (int, optional):
#         Quantidade de itens para serem gerados. Padrão é 10.
#         df_analistas (pl.DataFrame):
#         Polars DataFrame com os dados dos analistas.

#     Returns:
#         list[dict]:
#         Retorna uma lista de dicionários com os dados gerados.
#     """
#     return gerar_dados_tickets(qtd=qtd, df=df)


# if "tickets" not in ss:
#     ss.tickets = dados_tickets(qtd=10, df=ss.analistas)
# endregion

# region Transformar Dados
df_analistas: pl.DataFrame = processar_dados_random_user(ss.analistas)
df_analistas = df_analistas.with_columns(
    (pl.col("Nome") + " " + pl.col("Sobrenome")).alias("Analista"),
)
df_analistas = df_analistas["Foto", "Analista", "Email Empresarial", "Telefone"]
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

st.write("### Relação de Analistas")
config_colunas: dict[any, any] = {
    "Foto": st.column_config.ImageColumn(width="small"),
}


st.dataframe(data=df_analistas, column_config=config_colunas, width="content")
# endregion
