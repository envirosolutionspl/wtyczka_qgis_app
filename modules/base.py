
from . import utils
from PyQt5.QtWidgets import *


class BaseModule:
    """Klasa bazowa dla wszystkich modułów wtyczka_app.py"""
    listaOkienek = []
    activeDlg = None
    iface = None

    def openNewDialog(self, dlg):
        if self.activeDlg:
            self.activeDlg.close()
        self.activeDlg = dlg
        self.activeDlg.show()

    def showPopupValidationErrors(self, title, text, icon=QMessageBox.Warning):

        def saveErrorsFile(outputFile):
            with open(outputFile, 'w') as plik:
                plik.write(text)

        def saveErrors():
            plik = QFileDialog.getSaveFileName(filter="Pliki tekstowe (*.txt)")[0]
            if plik:
                try:
                    saveErrorsFile(plik)
                    self.iface.messageBar().pushSuccess("Eksport błędów:", "Zapisano plik z błędami.")
                except Exception as e:
                    self.iface.messageBar().pushCritical("Eksport błędów:", "Nie udało się zapisać pliku z błędami:" + str(e))

        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.Ok)
        raport = msg.addButton('Eksport błędów do pliku', QMessageBox.AcceptRole)
        raport.clicked.connect(saveErrors)
        return msg.exec_()

