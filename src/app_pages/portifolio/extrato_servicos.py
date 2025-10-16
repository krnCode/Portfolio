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
import xlsxwriter
from mockup_data.faker_data_generation import (
    gerar_dados_projeto,
    gerar_servicos_projeto,
)

st.set_page_config(
    page_title="Extrato de Serviços",
    layout="wide",
    menu_items={
        "Sobre": """
    PROBLEMA: Diversos analistas recebiam diversas solicitações de clientes para o envio
    de mais informações sobre os serviços prestados para entender a composição do que 
    foi cobrado. Os analistas precisavam encontrar as informações no sistema, extrair 
    relatórios, tratar, recalcular e confirmar se estava tudo correto, para então enviar
    ao cliente.

    SOLUÇÃO: Padronizamos o processo de análise e extração por meio de um painel que
    permite a visualização dos dados, a exportação em excel já formatado e recalculado,
    facilitando e agilizando o atendimento ao cliente.
    """,
    },
)

# region Funções
