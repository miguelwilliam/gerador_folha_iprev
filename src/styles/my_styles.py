from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

styles = getSampleStyleSheet()

estiloParagrafo1 = ParagraphStyle(
    "Compacto",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=7.5,
    leading=9,          # espaçamento entre linhas
    wordWrap="LTR",     # quebra de linha normal
)

estiloParagrafo2 = ParagraphStyle(
    "Compacto",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=7.5,
    leading=9,          # espaçamento entre linhas
    wordWrap="LTR",     # quebra de linha normal
    alignment=TA_CENTER
)

estiloParagrafo3 = ParagraphStyle(
    "Compacto",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=9,          # espaçamento entre linhas
    wordWrap="LTR",     # quebra de linha normal
    alignment=TA_CENTER
)

estiloTabela = [
    ('FONTSIZE', (0, 0), (-1, -1), 7.5),
    ('FONTNAME', (0, 0), (0, 2), 'Helvetica-Bold'),
    #('GRID', (0, 0), (-1, -1), 1, colors.black),

    # RETIRANDO CERTAS BORDAS:
    # ('BOX', (0, 0), (-1, -1), 1, colors.black), # não necessário
    ('BOX', (0, 0), (1, 2), 1, colors.black),
    ('GRID', (2, 0), (-1, -5), 1, colors.black),
    ('BOX', (0, 3), (1, 6), 1, colors.black),
    ('GRID', (0, 7), (1, 10), 1, colors.black),
    ('BOX', (0, 7), (-1, -1), 1, colors.black),

    # ALINHAMENTO :
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (2, 10), (2, 10), 'TOP'), # exceção, por algum motivo
    ('ALIGN', (-1, 0), (-1, -4), 'RIGHT'),
    ('ALIGN', (-1, 1), (-1, 2), 'CENTER'),

    ('SPAN', (0, 0), (1,0)),
    ('SPAN', (0, 1), (1,1)),
    ('SPAN', (0, 2), (1,2)),
    ('SPAN', (0, 3), (1,3)),
    ('SPAN', (0, 4), (1,4)),
    ('SPAN', (0, 5), (1,5)),
    ('SPAN', (0, 6), (1,6)),
    ('SPAN', (0, 8), (1,9)),
    ('SPAN', (0, 10), (1,10)),
    ('SPAN', (0, 11), (1,11)),
    ('SPAN', (0, 12), (1,12)),
    ('SPAN', (0, 13), (1,13)),
    ('SPAN', (2, 10), (-1, -1))
]