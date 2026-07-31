#from src.interface import interface
from src.testes import testes

def main():
    print('Rodando código principal...')
    meuExcel = testes.carregarPlanilhaComPaginas()
    df = meuExcel.carregar_pagina(meuExcel.paginas[-1])
    testes.teste_gerar_folha(meuExcel, df)



if __name__ == "__main__":
    main()