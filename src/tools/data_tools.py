"""
Arquivo para manter funções e itens para serem usados em outras partes do código,
com o objetivo de deixá-lo mais desacoplado e reutilizável.
"""

import xlsxwriter
import polars as pl
from io import BytesIO


def salvar_xlsx(df: pl.LazyFrame):
    """
    Função para salvar um dataframe em formato xlsx.
    Formatação do arquivo específico para o extrato de serviços por projeto.

    Args:
        df (pl.LazyFrame):
        Dataframe a ser salvo.

    Returns:
        BytesIO:
        Arquivo em formato xlsx salvo em um objeto BytesIO.
    """

    outuput = BytesIO()

    with xlsxwriter.Workbook(outuput) as wb:
        ws = wb.add_worksheet("extrato")

        title_bold = wb.add_format({"bold": True, "font_size": 30})

        ws.set_column("A:A", 3)
        ws.write("B2", "Extrato dos Serviços por Projeto", title_bold)

        df.write_excel(
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

    outuput.seek(0)

    return outuput
