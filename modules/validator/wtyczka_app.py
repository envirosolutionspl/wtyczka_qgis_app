# -*- coding: utf-8 -*-
from . import (WalidacjaDialog)
from .. import BaseModule
from ..utils import showPopup

from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtCore import Qt
import os


class ValidatorModule(BaseModule):

    def __init__(self, iface):
        self.iface = iface
        self.dataValidator = None   # inicjacja w głównym skrypcie wtyczki
        self.metadataValidator = None   # inicjacja w głównym skrypcie wtyczki
        # region okno moduł validator
        self.walidacjaDialog = WalidacjaDialog()
        # endregion

        # region eventy moduł validator
        #self.walidacjaDialog.prev_btn.clicked.connect(self.walidacjaDialog_prev_btn_clicked)

        self.walidacjaDialog.validate_btn.clicked.connect(self.walidacjaDialog_validate_btn_clicked)
        self.walidacjaDialog.validateGMLset_radioButton.toggled.connect(self.gmlset_checkBoxChangedAction)
        self.walidacjaDialog.validateGMLapp_radioButton.toggled.connect(self.gmlapp_checkBoxChangedAction)
        self.walidacjaDialog.validateXML_radioButton.toggled.connect(self.xml_checkBoxChangedAction)
        self.walidacjaDialog.close_btn.clicked.connect(self.walidacjaDialog.close)

        self.walidacjaDialog.chooseXML_widget.setFilter(filter="pliki XML (*.xml)")
        self.walidacjaDialog.chooseGMLset_widget.setFilter(filter="pliki XML/GML (*.xml *.gml)")
        self.walidacjaDialog.chooseGMLapp_widget.setFilter(filter="pliki XML/GML (*.xml *.gml)")
        # endregion

    """Event handlers"""
    # region walidacjaDialog
    def walidacjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def walidacjaDialog_validate_btn_clicked(self):

        if self.walidacjaDialog.validateGMLset_radioButton.isChecked():  # wybrano walidację GML dla zbioru
            path = self.walidacjaDialog.chooseGMLset_widget.filePath()
            if path:  # jest wybrany plik z danymi
                self.validateFile(path=path, validator=self.dataValidator, type='zbior')
            else:   # brak pliku z danymi
                self.iface.messageBar().pushWarning("Ostrzeżenie:", "Nie wskazano pliku z danymi.")

        elif self.walidacjaDialog.validateGMLapp_radioButton.isChecked():  # wybrano walidację GML dla app
            path = self.walidacjaDialog.chooseGMLapp_widget.filePath()
            if path:  # jest wybrany plik z danymi
                self.validateFile(path=path, validator=self.dataValidator, type='app')
            else:   # brak pliku z danymi
                self.iface.messageBar().pushWarning("Ostrzeżenie:", "Nie wskazano pliku z danymi.")

        elif self.walidacjaDialog.validateXML_radioButton.isChecked():    # wybrano walidację XML
            path = self.walidacjaDialog.chooseXML_widget.filePath()
            if path:  # jest wybrany plik z metadanymi
                self.validateFile(path=path, validator=self.metadataValidator, type='metadane')
            else:  # brak pliku z metadanymi
                self.iface.messageBar().pushWarning("Ostrzeżenie:", "Nie wskazano pliku z metadanymi.")

    def xml_checkBoxChangedAction(self, state):
        self.walidacjaDialog.chooseXML_widget.setEnabled(state)

    def gmlapp_checkBoxChangedAction(self, state):
        self.walidacjaDialog.chooseGMLapp_widget.setEnabled(state)

    def gmlset_checkBoxChangedAction(self, state):
        self.walidacjaDialog.chooseGMLset_widget.setEnabled(state)

    # endregion

    # """Helper methods"""
    # def __validateFile(self, path, validator):
    #     """walidacja pliku z danymi lub metadanymi"""
    #     if validator:  # walidator gotowy do dzialania
    #         validationResult = validator.validateXml(xmlPath=path)
    #         if validationResult[0]:  # poprawnie zwalidowano
    #             self.iface.messageBar().pushSuccess("Sukces:", "Pomyślnie zwalidowano plik. Nie wykryto błędów.")
    #             showPopup("Waliduj pliki", "Poprawnie zwalidowano plik.")
    #         else:   # błędy walidacji
    #             self.iface.messageBar().pushCritical("Błąd walidacji:", "Wykryto błędy walidacji.")
    #             self.showPopupValidationErrors("Błąd walidacji", "Wystąpiły błędy walidacji pliku:\n\n" + validationResult[1])
    #     else:  # walidator niegotowy do dzialania - nadal wczytuje XSD
    #         self.iface.messageBar().pushWarning("Ostrzeżenie:",
    #                                             "Schemat nie został jeszcze zaimportowany, spróbuj ponownie za chwilę.")

    """Popup windows"""
    def showPopupExport(self):
        showPopup("Wyeksportuj plik z błędami", "Poprawnie wyeksportowano plik z błędami.")


