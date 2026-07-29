from pathlib import Path
import pandas as pd
import re

ESTRUTURA = {
        'CELULAS': 
        {
            'NOME': 'A1',
            'ORGAO': 'B3',
        },

        'LINHAS': 
        {
            'COMPETENCIA': 5,
            'BASE_CALC': 8,
            'IPREV': 9,
            'PATRONAL': 13
        }
}

class Spreadsheet():
    def __init__(self, celulas:dict, linhas:dict, paginas:list):
        self.celulas = celulas
        self.linhas = linhas
        self.paginas = paginas
        self.estrutura = {
            'CELULAS':celulas, 
            'LINHAS':linhas
        }

        self._caminho = None

    @property
    def caminho(self):
        return self._caminho

    @caminho.setter
    def caminho(self, valor):

        if valor is None:
            self._caminho = None
            return

        path = Path(valor)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        if not path.is_file():
            raise ValueError("O caminho informado não é um arquivo.")

        if path.suffix.lower() not in (".xls", ".xlsx", ".xlsm"):
            raise ValueError("O arquivo deve ser do tipo Excel.")

        self._caminho = path

    def get_celula(self, campo):
        return self.celulas[campo]

    def get_linha(self, campo):
        return self.linhas[campo]

    def carregar_pagina(self, pagina):
        if pagina not in self.paginas and pagina > len(self.paginas)-1:
            raise ValueError(f"O índice ou nome da página não pertence às páginas dessa planilha: {[(self.paginas.index(x), x) for x in self.paginas]}")

        if self.caminho is None:
            raise ValueError("Nenhum arquivo foi definido.")

        if isinstance(pagina, int):
            pagina = self.paginas[pagina]

        return pd.read_excel(self.caminho, sheet_name=pagina, header=None)

    @staticmethod
    def excel_para_pandas(referencia: str) -> tuple[int, int]:
        """
        Converte uma referência do Excel (ex.: 'A1', 'B5', 'AA10')
        para índices do Pandas (linha, coluna).

        Exemplos:
            A1   -> (0, 0)
            B5   -> (4, 1)
            Z1   -> (0, 25)
            AA1  -> (0, 26)
            AB10 -> (9, 27)
        """

        match = re.fullmatch(r"([A-Za-z]+)(\d+)", referencia.strip())
        if not match:
            raise ValueError(f"Referência inválida: '{referencia}'")

        letras, linha = match.groups()

        # Converte as letras da coluna para número
        coluna = 0
        for letra in letras.upper():
            coluna = coluna * 26 + (ord(letra) - ord('A') + 1)

        return int(linha) - 1, coluna - 1