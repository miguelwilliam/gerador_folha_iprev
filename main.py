from src.interface import interface

def main():
    print('Rodando código principal...')
    app = interface.ExcelToPDFGUI()
    app.run()


if __name__ == "__main__":
    main()