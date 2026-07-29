from pathlib import Path
import sys

def resource_path(*parts):
    """
    Retorna o caminho absoluto de um recurso do projeto.
    Funciona tanto durante o desenvolvimento quanto com PyInstaller.
    """
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parents[2]

    return base.joinpath(*parts)