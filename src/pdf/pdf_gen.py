from datetime import datetime
import locale
from src.utils.paths import resource_path
from src.styles import my_styles
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.colors import lightgrey

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def gerarFolha(dados:dict, caminho_pdf, exclude_competencias:list=['BC'], competencias_dec_terc:list=['Jun', 'Dez']):
    """
    Gera o documento Guia da Previdência Própria com base na entrada de um dicionário de dados, na seguinte formatação:
    
    {
    NOME > João Silva
    ADMISSAO > dd/mm/YYYY
    ORGAO > Instituição
    1 > {'COMPETENCIA': 'Jan/26', 'BASE_CALC': 1783.1, 'IPREV': 249.63400000000001, 'PATRONAL': 282.26473}
    2 > {'COMPETENCIA': 'Fev/26', ...}
    }

    O parâmetro 'exclude_competencias' é uma lista de strings das competências serem puladas.
    """
    try:
        story = []

        # GERANDO IDENTIFICADOR (FC/FR) E VENDO SE EXISTE UMA ENTRADA DE DÉCIMO TERCEIRO
        admissao = datetime.strptime(dados['ADMISSAO'], '%d/%m/%Y')
        if admissao < datetime.strptime('31/12/2012', '%d/%m/%Y') or admissao > datetime.strptime('01/01/2025', '%d/%m/%Y'):
            identificador = 'FR - IPREV'
            # conta_corrente = '31.651-2'    
        else:
            identificador = 'FC - IPREV'
            # conta_corrente = '9197-9'

        chave_decimo_terceiro = next(
            (
                k for k, v in dados.items()
                if isinstance(v, dict) and '13' in str(v['COMPETENCIA'])
            ),
            None
        )

        # GERAR HEADER
        logo_path = resource_path("static", "img", "icon.png")
        header_img = Image(logo_path, 2*cm, 2*cm)

        dados_header = [
            [header_img, Paragraph('INST. PREVIDÊNCIA DE SÃO GONÇALO DO AMARANTE', my_styles.estiloParagrafo2), ''],
            ['', Paragraph('Extrato das Remunerações e Contribuições', my_styles.estiloParagrafo3), f'Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}']
        ]

        header = Table(dados_header, colWidths=[95, 285, 190])
        header.setStyle(TableStyle(my_styles.estiloHeader))

        story.append(header)
        story.append(Spacer(1, 0.5*cm))

        # GERAR TABELA DO SERVIDOR
        dados_servidor = [
            [Paragraph(f'Nome: {dados['NOME']}', my_styles.estiloParagrafo1), '', ''],
            [Paragraph(f'Fundo: {identificador}', my_styles.estiloParagrafo1), Paragraph(f'Admissão: {dados['ADMISSAO']}', my_styles.estiloParagrafo1), Paragraph(f'Data de cessão: {dados['CESSAO'].strftime("%d/%m/%Y")}', my_styles.estiloParagrafo1)],
            [Paragraph(f'Orgão: {dados['ORGAO']}', my_styles.estiloParagrafo1), '', '']
        ]

        tabela_servidor = Table(dados_servidor, colWidths=[190, 190, 190])
        tabela_servidor.setStyle(TableStyle(my_styles.estiloTabela1))

        story.append(tabela_servidor)
        story.append(Spacer(1, 0.5*cm))


        # GERAR TABELA EXTRATO
        dados_extrato = [
            ['Competência', 'Valor\nRemuneração', 'Valor\nContribuição', 'Valor\nRemuneração 13º', 'Valor\nContribuição 13º', 'Valor\nPatronal',  'TOTAL\nRemuneração + 13º']
        ]

        linha_total = ['TOTAL', 0, 0, 0, 0, 0, 0]
        contador_13 = 0
        
        for i in range(len(dados)-4):
            i = str(i+1)

            # PULAR PÁGINAS QUE EU EXCLUIR:
            if dados[i]['COMPETENCIA'] in exclude_competencias or i == chave_decimo_terceiro: 
                continue

            if dados[i]['COMPETENCIA'] in competencias_dec_terc and chave_decimo_terceiro != None:
                contador_13 += 1
                remun_13 = (dados[chave_decimo_terceiro]['BASE_CALC'])/len([item for item in competencias_dec_terc if item not in exclude_competencias])
                contrib_13 = (dados[chave_decimo_terceiro]['IPREV'])/len([item for item in competencias_dec_terc if item not in exclude_competencias])
                patronal_13 = 0
                if contador_13 == len(competencias_dec_terc):
                    patronal_13 =(dados[chave_decimo_terceiro]['PATRONAL'])
            else:
                remun_13, contrib_13, patronal_13 = 0, 0, 0


            '''linha = [
                dados[i]['COMPETENCIA'],
                f'{float(dados[i]['BASE_CALC']):,.2f}',
                f'{float(dados[i]['IPREV']):,.2f}',
                f'{float(remun_13):,.2f}',
                f'{float(contrib_13):,.2f}',
                f'{float(dados[i]['PATRONAL'] + patronal_13):,.2f}',
                f'{float(dados[i]['BASE_CALC'] + remun_13):,.2f}',
            ]'''
            linha = [
                dados[i]['COMPETENCIA'],
                locale.currency(dados[i]['BASE_CALC'], grouping=True, symbol=False),
                locale.currency(dados[i]['IPREV'], grouping=True, symbol=False),
                locale.currency(remun_13, grouping=True, symbol=False),
                locale.currency(contrib_13, grouping=True, symbol=False),
                locale.currency(dados[i]['PATRONAL'] + patronal_13, grouping=True, symbol=False),
                locale.currency(dados[i]['BASE_CALC'] + remun_13, grouping=True, symbol=False),
            ]

            linha_total[1] += dados[i]['BASE_CALC']
            linha_total[2] += dados[i]['IPREV']
            linha_total[3] += remun_13
            linha_total[4] += contrib_13
            linha_total[5] += dados[i]['PATRONAL'] + patronal_13
            linha_total[6] += dados[i]['BASE_CALC'] + remun_13


            dados_extrato.append(linha)

        # Formatando a linha de total
        for i in range(len(linha_total)):
            val = linha_total[i]
            if type(val) == str: 
                continue
            #linha_total[i] = f'{float(val):,.2f}'
            linha_total[i] = locale.currency(val, grouping=True, symbol=False)

        dados_extrato.append(linha_total)
            
        tabela_extrato = Table(dados_extrato, colWidths=[81, 81, 81, 81, 81, 81, 81])
        estilo_tabela = TableStyle(my_styles.estiloTabelaExtrato)

        # Adicionando estilo extra por cada linha da tabela
        for i in range(len(dados_extrato)-2):
            estilo_tabela.add('LINEBELOW', (0, i+1), (-1, i+1), 0.25, lightgrey)

        tabela_extrato.setStyle(estilo_tabela)

        story.append(tabela_extrato)
        

        pdf = SimpleDocTemplate(str(caminho_pdf), pagesize=A4, rightMargin=72, leftMargin=72, topMargin=36)

        pdf.build(story)

        print("PDF criado com sucesso!")    
        return True
    
    except Exception as e:
        print(f'ERRO EM GERAR O RELATÓRIO:\n{e}')
        return False