"""
Arquivo principal do projeto.
Será usado para controlar as páginas a serem exibidas no Streamlit.
"""

import streamlit as st

app_pages: dict[str, list[st.Page]] = {
    "Início": [
        st.Page("pagina_inicial.py", title="Página Inicial"),
        st.Page("sobre.py", title="Sobre"),
    ],
    "Portifolio": [
        st.Page("projects.py", title="Meus Projetos"),
    ],
}

pg: st.Page = st.navigation(app_pages)
