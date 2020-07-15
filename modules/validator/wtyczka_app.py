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

        # region okno moduł validator
        self.walidacjaDialog = WalidacjaDialog()
        # endregion

        # region eventy moduł validator
        #self.walidacjaDialog.prev_btn.clicked.connect(self.walidacjaDialog_prev_btn_clicked)

        self.walidacjaDialog.close_btn.setEnabled(False)
        self.walidacjaDialog.validate_btn.clicked.connect(self.walidacjaDialog_validate_btn_clicked)
        self.walidacjaDialog.validateGML_radioButton.toggled.connect(self.gml_checkBoxChangedAction)
        self.walidacjaDialog.validateXML_radioButton.toggled.connect(self.xml_checkBoxChangedAction)
        self.walidacjaDialog.close_btn.clicked.connect(self.walidacjaDialog.close)

        self.walidacjaDialog.chooseXML_widget.setFilter("*.xml")
        self.walidacjaDialog.chooseGML_widget.setFilter("*.gml")
        # endregion

    """Event handlers"""
    # region walidacjaDialog
    def walidacjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def walidacjaDialog_validate_btn_clicked(self):
        if self.dataValidator:  # walidator gotowy do dzialania
            validationResult = self.dataValidator.validateXml()
            if validationResult[0]:  # poprawnie zwalidowano
                print('OK')
                self.showPopupValid()
                self.walidacjaDialog.close_btn.setEnabled(True)
            else:
                print(validationResult[1])
                self.showPopupInvalid(validationResult[1])
        else: # walidator niegotowy do dzialania - nadal wczytuje XSD
            self.iface.messageBar().pushWarning("Ostrzeżenie:", "Schemat danych nie został jeszcze zaimportowany, spróbuj ponownie za chwilę.")


    def xml_checkBoxChangedAction(self, state):
        if self.walidacjaDialog.validateXML_radioButton.isChecked():
            self.walidacjaDialog.chooseXML_widget.setEnabled(True)
        else:
            self.walidacjaDialog.chooseXML_widget.setEnabled(False)

    def gml_checkBoxChangedAction(self, state):
        if self.walidacjaDialog.validateGML_radioButton.isChecked():
            self.walidacjaDialog.chooseGML_widget.setEnabled(True)
        else:
            self.walidacjaDialog.chooseGML_widget.setEnabled(False)
            # endregion

    """Helper methods"""

    """Popup windows"""
    def showPopupExport(self):
        showPopup("Wyeksportuj plik z błędami", "Poprawnie wyeksportowano plik z błędami.")

    def showPopupValid(self):
        showPopup("Waliduj pliki", "Poprawnie zwalidowano wszystkie wgrane pliki.")

    def showPopupInvalid(self, bledy):
        showPopup("Błąd walidacji", "Wystąpiły błędy walidacji pliku:\n\n" + bledy)