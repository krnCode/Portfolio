"""
Página inicial. Contém apenas boas vindas e o objetivo do projeto.
"""

import streamlit as st

st.set_page_config(page_title="Portfolio", layout="centered")

st.title("Sobre esta página")

st.markdown(
    """
    ### Olá, bem-vindo(a)!

    Este site foi criado para apresentar exemplos de soluções que já desenvolvi para:
    - Automatizar processos e aumentar produtividade
    - Criar painéis e visualizações de dados
    - Desenvolver soluções para problemas complexos
    - Otimizar fluxos de trabalho através de ferramentas personalizadas
    
    Cada página trará um exemplo do que foi criado, utilizando dados fictícios para 
    simular situações reais.
    """
)
