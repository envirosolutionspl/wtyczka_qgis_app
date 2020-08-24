# -*- coding: utf-8 -*-
from . import utils
from PyQt5.QtWidgets import *
from .utils import showPopup


class BaseModule:
    """Klasa bazowa dla wszystkich modułów wtyczka_app.py"""
    listaOkienek = []
    activeDlg = None
    iface = None

    """Helper methods"""

    def validateFile(self, path, validator, mute=False):
        """walidacja pliku z danymi lub metadanymi"""
        if validator:  # walidator gotowy do dzialania
            validationResult = validator.validateXml(xmlPath=path)
            if validationResult[0]:  # poprawnie zwalidowano
                self.iface.messageBar().pushSuccess(
                    "Sukces:", "Pomyślnie zwalidowano plik. Nie wykryto błędów.")
                if not mute:
                    showPopup("Waliduj pliki", "Poprawnie zwalidowano plik.")
                return True
            else:   # błędy walidacji
                self.iface.messageBar().pushCritical(
                    "Błąd walidacji:", "Wykryto błędy walidacji.")
                self.showPopupValidationErrors(
                    "Błąd walidacji", "Wystąpiły błędy walidacji pliku %s :\n\n%s" % (path, validationResult[1]))
                return False
        else:  # walidator niegotowy do dzialania - nadal wczytuje XSD
            self.iface.messageBar().pushWarning("Ostrzeżenie:",
                                                "Schemat walidacyjny nie został jeszcze zaimportowany, spróbuj ponownie za chwilę.")
            return False

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
            plik = QFileDialog.getSaveFileName(
                filter="Pliki tekstowe (*.txt)")[0]
            if plik:
                try:
                    saveErrorsFile(plik)
                    self.iface.messageBar().pushSuccess("Eksport błędów:", "Zapisano plik z błędami.")
                except Exception as e:
                    self.iface.messageBar().pushCritical(
                        "Eksport błędów:", "Nie udało się zapisać pliku z błędami:" + str(e))

        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.Ok)
        raport = msg.addButton('Eksport błędów do pliku',
                               QMessageBox.AcceptRole)
        raport.clicked.connect(saveErrors)
        return msg.exec_()
