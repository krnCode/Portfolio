"""
Este script contém utilitários para acessar APIs externas e extrair dados.
"""

import requests as r
import polars as pl

# region RandomUser.me


def buscar_dados_random_user(quantidade: int = 5) -> list[dict]:
    """
    Busca dados de usuários aleatórios no site RandomUser.me.
    Nacionalidade: BR

    Retorna apenas dados princiais:
    - Sexo
    - Nome
    - Email
    - ID
    - Foto


    Args:
        quantidade (int, optional):
        Quantidade de usuários a serem buscados. Padrão é 5.

    Returns:
        list[dict]:
        Retorna uma lista de dicionários com os dados de usuários.
    """
    url = f"https://randomuser.me/api/?results={quantidade}&nat=br?inc=name,phone,email,id,picture"

    try:
        response = r.get(url)
        response.raise_for_status()

        data = response.json()
        return data["results"]

    except r.RequestException as e:
        print(f"Erro ao buscar dados: {e}")
        return []


def processar_dados_random_user(dados: list[dict]) -> pl.DataFrame:
    """
    Processa os dados de usuários obtidos do site RandomUser.me.

    Args:
        dados (list[dict]):
        Lista de dicionários com os dados de usuários.

    Returns:
        pl.DataFrame:
        Retorna um DataFrame com os dados processados.
    """

    dados_processados = []

    for dado in dados:
        dado_processado = {
            "Nome": dado["name"]["first"],
            "Sobrenome": dado["name"]["last"],
            "Telefone": dado["phone"],
            "Email Empresarial": dado["email"],
            "Foto": dado["picture"],
        }

        dados_processados.append(dado_processado)

    df = pl.DataFrame(dados_processados)

    return df


# endregion

if __name__ == "__main__":
    # Testes
    usuarios = buscar_dados_random_user(1)
    print(usuarios)
    df = processar_dados_random_user(usuarios)
    print(df)
