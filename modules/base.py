# -*- coding: utf-8 -*-
from . import utils
from PyQt5.QtWidgets import *
from .utils import showPopup
from qgis.core import QgsApplication


class BaseModule:
    """Klasa bazowa dla wszystkich modułów wtyczka_app.py"""
    listaOkienek = []
    activeDlg = None
    iface = None
        # prepareXsdForApp = None
        # prepareXsdForMetadata = None

    """Helper methods"""

    def validateFile(self, path, validator, type):
        """walidacja pliku z danymi lub metadanymi"""
        taskDescriptions = [task.description() for task in QgsApplication.taskManager().activeTasks()]
        if validator:  # walidator gotowy do dzialania
            if type == 'metadane':
                validationResult = validator.validateMetadataXml(xmlPath=path)
            elif type == 'zbior':
                validationResult = validator.validateZbiorXml(xmlPath=path)
            elif type == 'app':
                validationResult = validator.validateAppXml(xmlPath=path)
            else:
                raise NotImplementedError
            if validationResult[0]:  # poprawnie zwalidowano
                self.iface.messageBar().pushSuccess(
                    "Sukces:", "Pomyślnie zwalidowano plik. Nie wykryto błędów.")
                showPopup("Waliduj pliki", "Poprawnie zwalidowano plik.")
                return True
            else:   # błędy walidacji
                self.iface.messageBar().pushCritical(
                    "Błąd walidacji:", "Wykryto błędy walidacji.")
                self.showPopupValidationErrors(
                    "Błąd walidacji", "Wystąpiły błędy walidacji pliku %s :\n\n%s" % (path, validationResult[1]))
                return False
        elif type == 'metadane':
            if 'Wczytywanie schematu XSD dla metadanych' in taskDescriptions:
                # walidator metadanych niegotowy do dzialania - nadal wczytuje XSD
                self.iface.messageBar().pushWarning("Ostrzeżenie:",
                                                    "Schemat walidacyjny metadanych nie został jeszcze zaimportowany, spróbuj ponownie za chwilę.")
                return False
            else:  # blad przy wczytywaniu - wczytac jeszcze raz
                self.showPopupYesNo(
                    "Ostrzeżenie:",
                    "Schemat walidacyjny metadanych nie został poprawnie zaimportowany.\nNIezbędne jest połączenie z internetem.\nCzy chcesz spóbować ponownie go zaimportować?",
                    lambda: self.prepareXsdForMetadata())
                return False
        elif type == 'zbior' or type == 'app':
            if 'Wczytywanie schematu XSD dla APP' in taskDescriptions:
                # walidator danych niegotowy do dzialania - nadal wczytuje XSD
                self.iface.messageBar().pushWarning("Ostrzeżenie:",
                                                    "Schemat walidacyjny APP i zbioru APP nie został jeszcze zaimportowany, spróbuj ponownie za chwilę.")
                return False
            else:  # blad przy wczytywaniu - wczytac jeszcze raz
                self.showPopupYesNo(
                    "Ostrzeżenie:",
                    "Schemat walidacyjny APP i zbioru APP nie został poprawnie zaimportowany.\nNIezbędne jest połączenie z internetem.\nCzy chcesz spóbować ponownie go zaimportować?",
                    lambda: self.prepareXsdForApp())
                return False
        else:
            raise NotImplementedError


    def openNewDialog(self, dlg):
        if self.activeDlg:
            self.activeDlg.close()
        self.activeDlg = dlg
        self.activeDlg.show()

    def showPopupYesNo(self, title, text, functionIfYes):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(text)
        yes = msg.addButton(
            'Tak', QMessageBox.AcceptRole)
        no = msg.addButton(
            'Nie', QMessageBox.RejectRole)
        msg.setDefaultButton(yes)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is yes:
            functionIfYes()

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
