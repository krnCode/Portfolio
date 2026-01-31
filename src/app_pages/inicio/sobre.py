"""
Página inicial.
Contém informações sobre o autor e sobre a página, com um breve resumo do itens que
compõem o Portfólio.
"""

import streamlit as st

st.set_page_config(page_title="Paulo Santana | Portfólio", layout="wide")

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


# region ----- Sidebar -------
with st.sidebar:
    language_options: list[str] = [
        "en-US",
        "pt-BR",
    ]
    images: list[str] = [
        "https://www.countryflags.com/wp-content/uploads/brazil-flag-png-large.png",  # BR
        "https://www.countryflags.com/wp-content/uploads/united-states-of-america-flag-png-large.png",  # US
    ]

    selected = st.radio(
        label="Language | Idioma",
        options=language_options,
        horizontal=True,
        index=1,
    )

    if selected == "pt-BR":
        st.image(image=images[0], width=150)
    elif selected == "en-US":
        st.image(image=images[1], width=150)
# endregion

col_hero_1, col_hero_2 = st.columns([2, 1], vertical_alignment="bottom")

# region ----- pt-BR -------
if selected == "pt-BR":
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
        **"Transformando cenários de dados complexos em ativos estratégicos para o 
        negócio."**
        
        Analista de Dados Sênior com mais de 10 anos de experiência conectando operações
        financeiras e tecnologia. Minha expertise consiste em converter dados 
        fragmentados e complexos em processos otimizados e insights acionáveis.

        Com passagens por empresas líderes de mercado, projeto soluções ponta a ponta,
        de pipelines de ETL robustos (Python, SQL, Polars/Pandas) a fluxos de automação 
        (RPA), garantindo a integridade dos dados e impulsionando a tomada de decisão 
        em alto nível.
        """
    )

    st.divider()

    st.subheader("🛠️ Sobre as Aplicações deste Portfólio")
    st.write(
        "Explore as soluções práticas desenvolvidas para desafios de negócio reais"
        "e projetos pessoais:"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏢 Portfólio | Casos de Negócio")
        st.markdown(
            """
        > * **Extrato de Serviços | Automação de Workflow & Reporting**  
        Fluxo automatizado para identificação de serviços faturáveis e geração de 
        relatórios profissionais, otimizando a eficiência administrativa.
        
        > * **Controle de Tickets | Analytics Operacional & Performance de CX**  
        Análise operacional focada em monitoramento de SLA e identificação de gargalos 
        para elevar a performance de Customer Experience (CX).
        """
        )

    with col2:
        st.markdown("#### 🧪 Projetos Pessoais")
        st.markdown(
            """
        > * **streamGlitch | Engenharia de Imagem & Manipulação de Arrays**  
        Aplicação interativa que utiliza Python (glitch_this) para manipulação avançada 
        de matrizes e processamento visual de dados.
        
        > * **Sapo Saver | Planejamento Financeiro & Analytics Preditivo**  
        Ferramenta de gestão patrimonial com projeções automáticas de poupança e 
        análise visual de 'Realizado vs. Orçado' para impulsionar a disciplina 
        financeira.
        """
        )

    st.write("")

    st.caption(
        "Desenvolvido 100% em Python com Streamlit • Dados fictícios utilizados para fins "
        "de demonstração."
    )

    st.divider()
# endregion

# region ----- en-US -------
else:
    with col_hero_1:
        st.markdown('<p class="hero-title">Paulo Santana</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <p class="hero-subtitle">Senior Data Analyst | Python, SQL, Dataviz and 
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
        📍 Ribeirão Preto, SP (Remote | Hybrid)
        
        🔗 [LinkedIn](https://www.linkedin.com/in/paulosanlkd/)
        🐙 [GitHub](https://github.com/krnCode)
        """
        )

    st.write("")

    st.markdown(
        """
        **"Transforming complex data landscapes into strategic business assets."**
        
        Senior Data Analyst with over 10 years of experience bridging the gap between
        financial operations and technology. I specialize in converting fragmented,
        complex data into streamlined processes and actionable insights.

        Having worked with industry-leading companies, I architect end-to-end
        solutions, from robust ETL pipelines (Python, SQL, Polars/Pandas) to RPA
        workflows, ensuring data integrity and empowering high-level decision-making.
        """
    )

    st.divider()

    st.subheader("🛠️ About the Applications of this Portfolio")
    st.write(
        "Navigate the sidebar to explore practical solutions that I have developed and "
        "my personal projects:"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏢 Portfolio | Business Cases")
        st.markdown(
            """
        > * **Service Statements | Workflow Automation & Reporting**  
        Automated workflow designed to identify billable 
        services and generate professional reports for client delivery, optimizing 
        administrative efficiency.
        
        > * **Ticket Dashboard | Operational Analytics & CX Performance**  
        Operational analytics focused on SLA monitoring and 
        process bottleneck identification to drive Customer Experience (CX) performance.
        """
        )

    with col2:
        st.markdown("#### 🧪 Personal Projects")
        st.markdown(
            """

        > * **streamGlitch | Image Engineering & Array Manipulation**  
        Interactive image engineering application leveraging Python
        (glitch_this) for advanced array manipulation and visual data processing.
        
        > * **Sapo Saver | Financial Planning & Predictive Analytics**  
        Personal wealth management tool featuring automated savings 
        projections and "Actual vs. Budget" visual analysis to drive financial 
        discipline.
        """
        )

    st.write("")

    st.caption(
        "Developed 100% in Python with Streamlit • Mock data used for demonstration "
    )

    st.divider()
# endregion
