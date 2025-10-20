"""
Arquivo principal do projeto.
Será usado para controlar as páginas a serem exibidas no Streamlit.
"""

import streamlit as st

app_pages: dict[str, list[st.Page]] = {
    "Início": [
        st.Page("./app_pages/inicio/sobre.py", title="Sobre"),
    ],
    "Portifolio": [
        st.Page(
            "./app_pages/portifolio/extrato_servicos.py", title="Extrato de Serviços"
        ),
        st.Page(
            "./app_pages/portifolio/controle_tickets.py", title="Controle de Tickets"
        ),
    ],
}

pg: st.Page = st.navigation(app_pages)
pg.run()
