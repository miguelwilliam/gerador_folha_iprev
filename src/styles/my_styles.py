from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

styles = getSampleStyleSheet()

estiloParagrafo1 = ParagraphStyle(
    "Compacto",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8,
    leading=9,          # espaçamento entre linhas
    wordWrap="LTR",     # quebra de linha normal
)

estiloParagrafo2 = ParagraphStyle(
    "Compacto",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9,
    leading=9,          # espaçamento entre linhas
    wordWrap="LTR",     # quebra de linha normal
)

estiloParagrafo3 = ParagraphStyle(
    "Compacto",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=9,          # espaçamento entre linhas
    wordWrap="LTR",     # quebra de linha normal
)

estiloHeader = [
    # FONTE
    ('FONTSIZE', (-1, -1), (-1, -1), estiloParagrafo2.fontSize),

    # BORDAS
    #('GRID', (0, 0), (-1, -1), 1, colors.black), # Para debug
    ('LINEBELOW', (1, -1), (-1, -1), 2, colors.HexColor('#135BA8')),

    # ALINHAMENTO
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    #('VALIGN', (1, 0), (1, 0), 'TOP'),
    ('ALIGN', (-1, -1), (-1, -1), 'RIGHT'),

    # SPAN
    ('SPAN', (0, 0), (0, 1)),
    ('SPAN', (1, 0), (-1, 0))
]

estiloTabela1 = [
    # BORDAS
    ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),

    # ALINHAMENTO
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

    # SPAN
    ('SPAN', (0, 0), (-1, 0)),
    ('SPAN', (0, -1), (-1, -1)),
]



estiloTabelaExtrato = [
    # FONTE
    ('FONTSIZE', (0, 0), (-1, -1), estiloParagrafo1.fontSize),

    # BORDAS
    ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#6fb3fc')),
    ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#6fb3fc')),

    # ALINHAMENTO
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),

    # BACKGROUND
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f2fc'))
]