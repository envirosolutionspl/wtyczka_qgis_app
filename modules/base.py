
from . import utils

class BaseModule:
    """Klasa bazowa dla wszystkich modułów wtyczka_app.py"""
    listaOkienek = []
    activeDlg = None

    def openNewDialog(self, dlg):
        if self.activeDlg:
            self.activeDlg.close()
        self.activeDlg = dlg
        self.activeDlg.show()

