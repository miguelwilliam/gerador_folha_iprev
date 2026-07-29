import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
from pathlib import Path

from src.utils.paths import resource_path
from src.pdf.pdf_gen import gerarGuia
from src.my_classes.spreadsheet import Spreadsheet, ESTRUTURA

class ExcelToPDFGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gerador de GPP")
        self.root.geometry("550x370")
        self.root.resizable(False, False)
        self.root.iconbitmap(resource_path("static", "img", "icon.ico"))

        self.competencias = {}
        self.multa_vars = {}

        self.create_widgets()

    def create_widgets(self):

        # Arquivo Excel
        tk.Label(self.root, text="Arquivo Excel:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        self.excel_path = tk.StringVar()

        tk.Entry(
            self.root,
            textvariable=self.excel_path,
            width=55
        ).grid(row=0, column=1)

        tk.Button(
            self.root,
            text="Selecionar",
            command=self.select_excel
        ).grid(row=0, column=2, padx=5)

        # Nome da planilha
        tk.Label(self.root, text="Planilha:").grid(row=1, column=0, padx=10, pady=10)

        self.combo_sheet = ttk.Combobox(
            self.root,
            state="readonly",
            width=40
        )

        self.combo_sheet.grid(row=1, column=1, sticky="w")

        self.combo_sheet.bind(
            "<<ComboboxSelected>>",
            self.on_sheet_changed
        )

        # Frame das competências
        self.frame_competencias = tk.LabelFrame(
            self.root,
            text="Competências"
        )

        self.frame_competencias.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        # Canvas
        self.canvas_comp = tk.Canvas(
            self.frame_competencias,
            height=100
        )

        # Barra de rolagem
        self.scrollbar_comp = tk.Scrollbar(
            self.frame_competencias,
            orient="vertical",
            command=self.canvas_comp.yview
        )

        self.canvas_comp.configure(
            yscrollcommand=self.scrollbar_comp.set
        )

        # Frame que conterá os checkboxes
        self.frame_checks = tk.Frame(self.canvas_comp)
        self.frame_checks.grid_columnconfigure(0, weight=1)

        self.canvas_comp.create_window(
            (0, 0),
            window=self.frame_checks,
            anchor="nw"
        )

        # Atualiza a área rolável sempre que o conteúdo muda
        self.frame_checks.bind(
            "<Configure>",
            lambda e: self.canvas_comp.configure(
                scrollregion=self.canvas_comp.bbox("all")
            )
        )

        self.frame_checks.bind("<Enter>", self._bind_mousewheel)
        self.frame_checks.bind("<Leave>", self._unbind_mousewheel)

        self.canvas_comp.bind("<Enter>", self._bind_mousewheel)
        self.canvas_comp.bind("<Leave>", self._unbind_mousewheel)

        self.canvas_comp.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar_comp.pack(
            side="right",
            fill="y"
        )

        # Nome do PDF
        tk.Label(self.root, text="Nome do PDF:").grid(
            row=3, column=0, padx=10, pady=10, sticky="w"
        )

        self.pdf_name = tk.StringVar()

        tk.Entry(
            self.root,
            textvariable=self.pdf_name,
            width=30
        ).grid(row=3, column=1, sticky="w")

        # Pasta de saída
        tk.Label(self.root, text="Pasta de saída:").grid(
            row=4, column=0, padx=10, pady=10, sticky="w"
        )

        self.output_path = tk.StringVar()

        tk.Entry(
            self.root,
            textvariable=self.output_path,
            width=55
        ).grid(row=4, column=1)

        tk.Button(
            self.root,
            text="Selecionar",
            command=self.select_output
        ).grid(row=4, column=2, padx=5)

        # Botão principal
        tk.Button(
            self.root,
            text="Converter",
            width=20,
            command=self.convert
        ).grid(row=5, column=1, pady=25)

    def atualizar_competencias(self, competencias):
        # Remove os checkboxes antigos
        for widget in self.frame_checks.winfo_children():
            widget.destroy()

        self.competencias.clear()

        tk.Label(
            self.frame_checks,
            text="Competência",
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=0, sticky="w", padx=5)

        tk.Label(
            self.frame_checks,
            text="Multa (R$)",
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=1, padx=5)

        # Cria novos checkboxes
        for i, competencia in enumerate(competencias):

            check_var = tk.BooleanVar(value=True)
            multa_var = tk.StringVar()

            chk = tk.Checkbutton(
                self.frame_checks,
                text=competencia,
                variable=check_var
            )

            entry = tk.Entry(
                self.frame_checks,
                textvariable=multa_var,
                width=10,
                justify="right"
            )

            chk.grid(
                row=i+1,
                column=0,
                sticky="w",
                padx=5,
                pady=2
            )

            entry.grid(
                row=i+1,
                column=1,
                padx=5
            )

            self.competencias[competencia] = {
                "checked": check_var,
                "multa": multa_var
            }

        self.frame_checks.update_idletasks()

        self.canvas_comp.configure(
            scrollregion=self.canvas_comp.bbox("all")
        )

    def pegar_competencias(self, filename, sheetname):
        #Chamar a atualização de competencias   
        meuExcel = Spreadsheet(ESTRUTURA['CELULAS'], ESTRUTURA['LINHAS'], paginas=pd.ExcelFile(filename).sheet_names)
        meuExcel.caminho = filename

        df = meuExcel.carregar_pagina(sheetname)

        competencias = []
        for col in range(len(df.columns)):
            if col == 0: continue
            pos_pandas = [meuExcel.linhas['COMPETENCIA']-1, col]
            
            competencias.append(df.iloc[pos_pandas[0], pos_pandas[1]])

        return competencias

    def select_excel(self):
        filename = filedialog.askopenfilename(
            title="Selecione um arquivo Excel",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )

        if not filename:
            return

        self.excel_path.set(filename)

        xls = pd.ExcelFile(filename)

        self.combo_sheet["values"] = xls.sheet_names

        if xls.sheet_names:
            self.combo_sheet.current(0)

        competencias = self.pegar_competencias(filename = filename, sheetname = xls.sheet_names[0])

        self.atualizar_competencias(competencias)

    def on_sheet_changed(self, event):
        competencias = self.pegar_competencias(
            self.excel_path.get(),
            self.combo_sheet.get()
        )

        self.atualizar_competencias(competencias)

    def select_output(self):
        folder = filedialog.askdirectory(
            title="Selecione a pasta de saída"
        )

        if folder:
            self.output_path.set(folder)

    def convert(self):

        excel = self.excel_path.get().strip()
        sheet = self.combo_sheet.get()
        pdf = self.pdf_name.get().strip()
        output = self.output_path.get().strip()
        competencias_nao_selecionadas = [
            competencia
            for competencia, dados in self.competencias.items()
            if not dados["checked"].get()
        ]

        competencias = []

        multas = {}

        for competencia, dados in self.competencias.items():

            if dados["checked"].get():

                competencias.append(competencia)

                texto = dados["multa"].get().strip()

                if texto:
                    multas[competencia] = float(
                        texto.replace(",", ".")
                    )

        if not excel:
            messagebox.showerror("Erro", "Selecione um arquivo Excel.")
            return

        if not sheet:
            messagebox.showerror("Erro", "Informe o nome da planilha.")
            return

        if not pdf:
            messagebox.showerror("Erro", "Informe o nome do PDF.")
            return

        if not output:
            messagebox.showerror("Erro", "Selecione a pasta de saída.")
            return

        pdf_path = Path(output) / f"{pdf}.pdf"

        # ==================================================
        # Coloque aqui sua lógica de conversão Excel -> PDF
        # ==================================================
        
        meuExcel = Spreadsheet(ESTRUTURA['CELULAS'], ESTRUTURA['LINHAS'], paginas=pd.ExcelFile(excel).sheet_names)
        meuExcel.caminho = excel
        df = meuExcel.carregar_pagina(sheet)
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

            if dados[str(col)]['COMPETENCIA'] in multas.keys():
                dados[str(col)]['MULTA'] = multas[dados[str(col)]['COMPETENCIA']]

        for chave, valor in dados.items(): print(f'{chave} > {valor}')

        sucesso = gerarGuia(dados, pdf_path, competencias_nao_selecionadas)
        print('SUCESSO:',sucesso)

        if sucesso:
            messagebox.showinfo(
            "Dados informados",
            f"""Excel:
{excel}

Planilha:
{sheet}

PDF:
{pdf_path}
"""
        )
        else:
            messagebox.showinfo("Erro", "Um erro aconteceu na geração do seu relatório. Cheque as suas configurações antes de tentar novamente.")

    def _on_mousewheel(self, event):
        self.canvas_comp.yview_scroll(
            int(-event.delta / 120),
            "units"
        )

    def _bind_mousewheel(self, event):
        self.canvas_comp.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas_comp.unbind_all("<MouseWheel>")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ExcelToPDFGUI()
    app.run()