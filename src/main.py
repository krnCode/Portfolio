"""
Arquivo principal do projeto.
Será usado para controlar as páginas a serem exibidas no Streamlit.
"""

import streamlit as st

app_pages: dict[str, list[st.Page]] = {
    "Início": [
        st.Page("./app_pages/inicio/sobre.py", title="Sobre"),
    ],
    "Portfolio": [
        st.Page(
            "./app_pages/portifolio/extrato_servicos.py", title="Extrato de Serviços"
        ),
        st.Page(
            "./app_pages/portifolio/controle_tickets.py", title="Controle de Tickets"
        ),
    ],
    "Projetos Pessoais": [
        st.Page("./app_pages/projetos_pessoais/streamglitch.py", title="streamGlitCH"),
        st.Page("./app_pages/projetos_pessoais/sapo_saver.py", title="Sapo Saver"),
        # st.Page("./app_pages/projetos_pessoais/qftb.py", title="Quest for the Best"),
    ],
}

pg: st.Page = st.navigation(app_pages)
pg.run()
