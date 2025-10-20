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

from tools.api_data import buscar_dados_random_user, processar_dados_random_user

# region Config Página
# Nesta seção é definido o título da página, o layout e os itens de menu - itens para
# explicar o projeto, com o problema e a solução adotada.
st.set_page_config(
    page_title="Controle de tickets",
    layout="wide",
    menu_items={
        "About": """
    PROBLEMA:
    Diaramente o time recebe tickets por meio de uma plataforma para atenderem 
    solicitações de clientes ou de áreas internas. Para que a gerencia possa controlar
    o andamento dos tickets, era necessário extrair os relatórios da plataforma, 
    tratá-los, incluir na ferramenta de BI validar e atualizar os dados na ferramenta
    de BI, o que consumia muito tempo, e também não trazia as informações atualizadas.


    SOLUÇÃO:
    Criamos um painel que acessa a API da plataforma de tickets, retorna os dados 
    necessários, já trata os dados e realiza uma atualização automática quando 
    necessário, assim provendo de informações mais atualizadas.
    Também foi criado uma sessão para cada analista poder consultar o status de seus
    tickets, podendo selecionar seu nome e visualizar informações gerenciais somente 
    sobre os tickets que ele está responsável.
    """,
    },
)
# endregion

# region Gerar
analistas = buscar_dados_random_user(10)
df_analistas = processar_dados_random_user(analistas)

print(df_analistas)
# endregion
