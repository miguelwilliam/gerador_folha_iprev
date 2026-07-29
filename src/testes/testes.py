import os
from dotenv import load_dotenv

from src.my_classes.spreadsheet import Spreadsheet, ESTRUTURA
from src.pdf.pdf_gen import gerarGuia

def carregarPlanilha():
    load_dotenv()

    meuExcel = Spreadsheet(
        celulas=ESTRUTURA['CELULAS'], 
        linhas=ESTRUTURA['LINHAS'], 
        paginas=['ALIQUOTA', 'CLAUDETE', 'JUNIOR']
        )

    meuExcel.caminho = os.getenv('CAMINHO')
    df = meuExcel.carregar_pagina(1) 
    return meuExcel, df


# Bloco de teste de leitura do excel:
def teste_leitura(meuExcel, df):
    for celula, pos in meuExcel.celulas.items():
        pos_pandas = Spreadsheet.excel_para_pandas(pos)

        # Para extrair o nome da célula
        if celula == 'NOME':
            dados = str(df.iloc[pos_pandas[0], pos_pandas[1]]).split(' - ')
            print(f'NOME, {pos_pandas} > {dados[0]}')
            print(f'DATA DE ADMISSÃO, {pos_pandas} > {dados[1]}')
            continue

        print(f'{celula}, {pos_pandas} > {df.iloc[pos_pandas[0], pos_pandas[1]]}')

    for col in range(len(df.columns)):
        if col == 0: continue

        print('==================')
        for dado, linha in meuExcel.linhas.items():
            pos_pandas = [linha-1, col]
            
            # print(f'{dado}, ({linha-1}, {col}) > {df.iloc[pos_pandas[0], pos_pandas[1]]}')
            print(f'{dado} > {df.iloc[pos_pandas[0], pos_pandas[1]]}')

# Teste com formatação de dados no python

def teste_gerar_documento(meuExcel, df):
    dados = {}

    for celula, pos in meuExcel.celulas.items():
        pos_pandas = Spreadsheet.excel_para_pandas(pos)

        # Para extrair o nome da célula
        if celula == 'NOME':
            dados_excel = str(df.iloc[pos_pandas[0], pos_pandas[1]]).split(' - ')
            dados['NOME'] = dados_excel[0]
            dados['ADMISSAO'] = dados_excel[1].split(' ')[1]
            continue

        dados[str(celula)] = df.iloc[pos_pandas[0], pos_pandas[1]]

    for col in range(len(df.columns)):
        if col == 0: continue

        dados[str(col)] = {}

        for dado, linha in meuExcel.linhas.items():
            pos_pandas = [linha-1, col]
            
            # print(f'{dado}, ({linha-1}, {col}) > {df.iloc[pos_pandas[0], pos_pandas[1]]}')
            # print(f'{dado} > {df.iloc[pos_pandas[0], pos_pandas[1]]}')
            dados[str(col)][dado] = df.iloc[pos_pandas[0], pos_pandas[1]]

    for chave, valor in dados.items(): print(f'{chave} > {valor}')

    
    #sucesso = gerarGuia(dados, r'./relatorio_teste.pdf')
    #print('SUCESSO:', sucesso)

