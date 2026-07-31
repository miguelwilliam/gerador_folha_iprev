import os
from dotenv import load_dotenv

from src.my_classes.spreadsheet import Spreadsheet, ESTRUTURA
from src.pdf.pdf_gen import gerarFolha

def carregarPlanilhaComPaginas():
    load_dotenv()

    meuExcel = Spreadsheet(
        celulas=ESTRUTURA['CELULAS'], 
        linhas=ESTRUTURA['LINHAS']
        )

    meuExcel.caminho = os.getenv('CAMINHO')
    meuExcel.carregar_paginas_automaticamente()

    print(meuExcel.paginas)
    return meuExcel


# Teste com formatação de dados no python

def teste_gerar_folha(meuExcel, df):
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

    gerarFolha(dados, 'relatorio.pdf', ['BC'])