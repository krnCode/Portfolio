"""
Projeto: Sapo Saver
Objetivo: Ajudar o usuário a visualizar e controlar finanças pessoais
"""

import streamlit as st

st.set_page_config(page_title="Sapo Saver", layout="wide")

st.title("Sapo Saver")
st.divider()

with st.expander(label="Sobre este projeto", expanded=False):

    col1, col2 = st.columns(spec=2, gap="small", border=True)
    with col1:
        st.markdown(
            """
            ### **Objetivo**
            Criar um painel interativo para o usuário poder visualizar suas finanças
            com maior facilidade.

            O app proporciona um template para ser utilizado e preenchido pelo usuário

            ### **Aprendizados**
            Neste projeto foi possível colocar em prática transformação de dados em
            informações visuais, com gráficos e informações relevantes na questão de 
            finanças pessoais.
            """
        )

    with col2:
        st.markdown(
            """
            ### Tech
            * Streamlit
            * Pandas
            * Altair
            * Python

            ### Como utilizar
            1) Acesse a página do app;
            2) Baixar a planilha template na aba "Criar Planilha";
            3) Após preencher a planilha com os gastos, fazer o upload da planilha na
            aba "Análise dos Gastos" na parte lateral ("Drag and drop file here")
            """
        )

    st.write("### Exemplo Visual")
    st.image(image="src/res/sapo_saver_sample.png", width="content")

st.markdown(
    """
    ## **Links do projeto e mais**

    - 🐸 [Sapo Saver](https://saposaver.streamlit.app)
    - 💻 [GitHub](https://github.com/krnCode/SapoSaver)
    - 🔗 [LinkedIn](https://www.linkedin.com/in/paulosanlkd/)

    """
)
