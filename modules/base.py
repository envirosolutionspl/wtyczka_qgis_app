class BaseModule:
    listaOkienek = []
    activeDlg = None

    def openNewDialog(self, dlg):
        if self.activeDlg:
            self.activeDlg.close()
        self.activeDlg = dlg
        self.activeDlg.show()