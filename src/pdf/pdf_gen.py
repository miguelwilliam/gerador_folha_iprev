from datetime import datetime

from src.styles import my_styles
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer



def gerarFolha(dados:dict, caminho_pdf, exclude_competencias:list=['BC']):
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

        # GERANDO IDENTIFICADOR (FC/FR)
        admissao = datetime.strptime(dados['ADMISSAO'], '%d/%m/%Y')
        if admissao < datetime.strptime('31/12/2012', '%d/%m/%Y') or admissao > datetime.strptime('01/01/2025', '%d/%m/%Y'):
            identificador = 'FR - IPREV'
            # conta_corrente = '31.651-2'    
        else:
            identificador = 'FC - IPREV'
            # conta_corrente = '9197-9'

        # GERAR HEADER
        logo_path = 'static/img/icon.png'
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

        '''
        for i in range(len(dados)-3):
            i = str(i+1)

            # PULAR PÁGINAS QUE EU EXCLUIR:
            if dados[i]['COMPETENCIA'] in exclude_competencias: 
                continue

            # PROCURAR VALOR DE MULTA EXISTENTE NOS DADOS
            try:
                multa = dados[i]['MULTA']
            except:
                multa = 0
            
            dados_tabela = [
                
            ]

            tabela = Table(dados_tabela, colWidths=[95,285,95,95])
    
            tabela.setStyle(TableStyle(my_styles.estiloTabela))

            story.append(tabela)
        '''

        # ADICIONAR OS VALORES PARA CADA FUNCIONÁRIO

        # ADICIONAR VALORES DE SOMA NO FINAL DA TABELA

        pdf = SimpleDocTemplate(str(caminho_pdf), pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72)

        pdf.build(story)

        print("PDF criado com sucesso!")
        return True
    
    except Exception as e:
        print(f'ERRO EM GERAR O RELATÓRIO:\n{e}')
        return False