"""
Este script gera dados sintéticos (não reais) para serem utilizados neste projeto.
"""

from faker import Faker
import xlsxwriter
import polars as pl
import random

fk_en: Faker = Faker("en_US")
fk_br: Faker = Faker("pt_BR")


# region Extrato Serviços
def gerar_dados_projeto(
    qtd_itens: int = 50,
    qtd_projetos: int = 20,
    qtd_clientes: int = 20,
) -> list[dict]:
    """
    Gera dados sintéticos com a quantidade informada, sendo o padrão 50 itens.
    Contém as seguintes colunas:
    - ID Projeto: str
    - Nome Projeto: str
    - Data Criação Projeto: datetime (de 5 anos atrás até hoje)
    - ID Cliente: str
    - Nome Cliente: str
    - CNPJ Cliente: str
    - Taxa/Hora Contratada: int (50 a 500)

    Args:
        qtd_itens (int, optional):
        Quantidade de itens para serem gerados. Padrão é 50.

        qtd_projetos (int, optional):
        Quantidade de projetos únicos para serem gerados. Padrão é 20.

        qtd_clientes (int, optional):
        Quantidade de clientes únicos para serem gerados. Padrão é 20.

    Returns:
        list[dict]: Retorna uma lista de dicionários com os dados gerados.
    """
    return [
        {
            "ID Projeto": "PROJ" + str(random.randint(1, qtd_projetos)).zfill(10),
            "Nome Projeto": " ".join(fk_en.words(3)).title(),
            "Data Criação Projeto": fk_br.date_time_between(
                start_date="-5y", end_date="now"
            ),
            "ID Cliente": "CLI" + str(random.randint(1, qtd_clientes)).zfill(10),
            "Nome Cliente": fk_br.unique.company(),
            "CNPJ Cliente": fk_br.unique.cnpj(),
            "Taxa/Hora Contratada": random.randint(50, 500),
        }
        for i in range(qtd_itens)
    ]


def gerar_servicos_projeto(
    projeto: dict,
    qtd_servicos: int = 20,
) -> dict:
    """
    Gera dados sintéticos contendo a descrição dos serviços realizados para o projeto.

    contém as seguintes colunas:
    - Projeto Vinculado: str
    - ID Serviço: str
    - Descrição Serviço: str (60 caracteres)
    - Responsável pelo Serviço: str (30 caracteres)
    - QTD Horas: int (1 a 10)
    - Data Serviço: datetime (de 5 anos atrás até hoje)

    Args:
        projeto (dict):
        Dicionário com os dados do projeto vinculado ao serviço.

        qtd_servicos (int, optional):
        Quantidade de itens para serem gerados. Padrão é 20.

    Returns:
        dict: Retorna um dicionário com os dados gerados.
    """
    return {
        "Projeto Vinculado": projeto["ID Projeto"],
        "ID Serviço": "SERV" + str(random.randint(1, qtd_servicos)).zfill(10),
        "Descrição Serviço": fk_en.text(max_nb_chars=60),
        "Responsável pelo Serviço": fk_br.name(),
        "QTD Horas": random.randint(1, 10),
        "Data Serviço": fk_br.date_time_between(
            start_date=projeto["Data Criação Projeto"], end_date="now"
        ),
    }


# endregion


if __name__ == "__main__":
    # Teste rápido para visualizar os dados gerados
    dados_projeto: list[dict] = gerar_dados_projeto(
        qtd_itens=159, qtd_projetos=360, qtd_clientes=254
    )
    servicos_projeto: list[dict] = [
        gerar_servicos_projeto(projeto=projeto, qtd_servicos=500)
        for projeto in dados_projeto
        for i in range(random.randint(1, 20))
    ]

    df_projetos: pl.LazyFrame = pl.LazyFrame(dados_projeto)
    df_servicos: pl.LazyFrame = pl.LazyFrame(servicos_projeto)

    # print(df_projetos)
    # print(df_servicos)

    df_servicos_taxahora: pl.LazyFrame = (
        df_servicos.join(
            other=df_projetos,
            left_on="Projeto Vinculado",
            right_on="ID Projeto",
            how="inner",
        )
        .with_columns(
            (pl.col("QTD Horas") * pl.col("Taxa/Hora Contratada")).alias(
                "Custo Serviço"
            )
        )
        .sort(
            by=["Projeto Vinculado", "Data Serviço"],
            descending=[False, False],
        )
    )

    df_final: pl.LazyFrame = df_servicos_taxahora.collect()

    print(df_final)

    with xlsxwriter.Workbook(r"C:\Users\conta\Desktop\extrato_servicos.xlsx") as wb:
        ws = wb.add_worksheet("extrato")

        title_bold = wb.add_format({"bold": True, "font_size": 30})

        ws.set_column("A:A", 3)
        ws.write("B2", "Extrato dos Serviços por Projeto", title_bold)

        df_final.write_excel(
            workbook=wb,
            worksheet=ws,
            position="B4",
            table_style="Table Style Light 1",
            header_format={
                "bold": True,
                "font_color": "white",
                "bg_color": "#0B092C",
            },
            column_totals=["QTD Horas", "Custo Serviço"],
            autofit=True,
            hide_gridlines=True,
        )
