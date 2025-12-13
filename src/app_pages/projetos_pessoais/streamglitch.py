"""
Projeto: streamGlitCH
Objetivo: Gerar efeitos de distorção de imagem estilo "glitch" em fotos enviadas pelo
usuário
"""

import streamlit as st

st.set_page_config(page_title="streamGlitCH", layout="wide")

st.title("streamGlitCH")
st.divider()

with st.expander(label="Sobre este projeto", expanded=False):

    col1, col2 = st.columns(spec=2, gap="small", border=True)
    with col1:
        st.markdown(
            """
            ### **Objetivo**
            Criar uma interface utilizando streamlit para que o usuário possa selecionar
            os efeitos disponíveis na biblioteca glitch_this sem que seja necessário
            acessar CLI (um terminal utilizando linhas de comando).

            Além de gerar imagens estáticas, o app também gera um gif da imagem.

            ### **Aprendizados**
            Neste projeto foi possível colocar em prática a disponibilização de filtros
            e opções para o usuário final gerar a imagem que deseja criar sem a
            necessidade de utilizar linhas de comando, facilitando o acesso a este 
            recurso para o usuário final.
            """
        )

    with col2:
        st.markdown(
            """
            ### Tech
            * Streamlit
            * glitch_this
            * PIL
            * Python

            ### Como utilizar
            1) Acesse a página do app;
            2) Na barra lateral, arrastar uma foto qualquer na caixa "Drag and drop 
            files here";
            3) Após ter enviado a foto, selecionar as opções disponíveis e ver o 
            resultado na nova foto gerada.
            """
        )

    st.write("### Exemplo Visual")
    st.image(image="src/res/streamglitch_sample.png", width="content")

st.markdown(
    """
    ## **Links do projeto e mais**

    - 🌐 [streamGlitCH](https://streamglitch.streamlit.app)
    - 💻 [GitHub](https://github.com/krnCode/streamGlitCH)
    - 🔗 [LinkedIn](https://www.linkedin.com/in/paulosanlkd/)

    """
)
