"""
Página inicial. Contém apenas boas vindas e o objetivo do projeto.
"""

import streamlit as st

st.set_page_config(page_title="Paulo Santana | Portfolio", layout="wide")

st.markdown(
    """
    <style>
        .block-container {padding-top: 2rem; padding-bottom: 2rem;}
        .badge {
            background-color: #f0f2f676;
            color: #31333F;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: 600;
            font-size: 14px;
            margin-right: 5px;
            border: 1px solid #e6e9ef;
        }
        .hero-title {
            font-size: 42px !important;
            font-weight: 700 !important;
            margin-bottom: 0px !important;
        }
        .hero-subtitle {
            font-size: 20px !important;
            color: #555;
            margin-bottom: 20px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

col_hero_1, col_hero_2 = st.columns([2, 1], vertical_alignment="bottom")

with col_hero_1:
    st.markdown('<p class="hero-title">Paulo Santana</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="hero-subtitle">Analista de Dados Sênior | Python, SQL, Dataviz e 
        ETL</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div>
            <span class="badge">🐍 Python/SQL</span>
            <span class="badge">🔍 Business Intelligence</span>
            <span class="badge">📈 Finance</span>
            <span class="badge">📊 Data Visualization</span>
            <span class="badge">📑 ETL</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col_hero_2:
    st.info(
        """
    📍 Ribeirão Preto, SP (Remoto | Hibrido)
    
    🔗 [LinkedIn](https://www.linkedin.com/in/paulosanlkd/)
    🐙 [GitHub](https://github.com/krnCode)
    """
    )

st.write("")

st.markdown(
    """
    **"Transformando dados e operações em estratégia."**
    
    Sou Analista de Dados e possuo background na área contábil e de negócios, onde 
    atuei por mais de 10 anos. Meu objetivo principal é transformar o caos de dados 
    complexos em estratégias claras e processos eficientes.

    Com passagens em grandes empresas, tenho experiência em construir soluções que vão 
    além do visual, como pipelines de dados e automações (ETL/RPA) utilizando Python, 
    SQL, Polars ou Pandas, garantindo que a informação seja íntegra e acionável.
    """
)

st.divider()

st.subheader("🛠️ Sobre as Aplicações deste Portfólio")
st.write("Navegue pelo menu lateral para explorar soluções práticas que desenvolvi:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🏢 Portfólio | Casos de Negócio")
    st.markdown(
        """
    * **Extrato de Serviços:** Automação de conciliação financeira e detecção de 
    anomalias em faturamentos.
    
    * **Controle de Tickets:** Dashboard operacional focado em SLA e gargalos de 
    atendimento (Customer Experience).
    """
    )

with col2:
    st.markdown("#### 🧪 Projetos Pessoais")
    st.markdown(
        """
    * **streamGlitch:** Engenharia de imagens e manipulação de arrays via Python 
    (biblioteca glitch_this), com interface interativa.
    
    * **Sapo Saver:** Aplicação de gestão orçamentária pessoal com visualização gráfica
    de *Realizado vs Orçado* e projeção automática de saldo (Saving).
    """
    )

st.write("")

st.caption(
    "Desenvolvido 100% em Python com Streamlit • Dados fictícios utilizados para fins "
    "de demonstração."
)


st.divider()


# st.title("Sobre esta página")

# st.markdown(
#     """
#     ### Olá, bem-vindo(a)!

#     Este site foi criado para apresentar exemplos de soluções que já desenvolvi para:
#     - Automatizar processos e aumentar produtividade
#     - Criar painéis e visualizações de dados
#     - Desenvolver soluções para problemas complexos
#     - Otimizar fluxos de trabalho através de ferramentas personalizadas

#     Cada página trará um exemplo do que foi criado, utilizando dados fictícios para
#     simular situações reais.
#     """
# )
