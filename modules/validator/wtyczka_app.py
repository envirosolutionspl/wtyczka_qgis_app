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
        self.walidacjaDialog.chooseGML_widget.setFilter("*.gml; *.xml")
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
                self.iface.messageBar().pushSuccess("Sukces:",
                                                    "Pomyślnie zwalidowano plik. Nie wykryto błędów.")
            else:
                # print(validationResult[1])
                self.showPopupInvalid(validationResult[1])
                self.iface.messageBar().pushCritical("Błąd walidacji:",
                                                    "Wykryto błędy walidacji.")
        else: # walidator niegotowy do dzialania - nadal wczytuje XSD
            self.iface.messageBar().pushWarning("Ostrzeżenie:", "Schemat danych nie został jeszcze zaimportowany, spróbuj ponownie za chwilę.")


    def xml_checkBoxChangedAction(self, state):
        self.walidacjaDialog.chooseXML_widget.setEnabled(state)

    def gml_checkBoxChangedAction(self, state):
        self.walidacjaDialog.chooseGML_widget.setEnabled(state)

    # endregion

    """Helper methods"""

    """Popup windows"""
    def showPopupExport(self):
        showPopup("Wyeksportuj plik z błędami", "Poprawnie wyeksportowano plik z błędami.")

    def showPopupValid(self):
        showPopup("Waliduj pliki", "Poprawnie zwalidowano wszystkie wgrane pliki.")

    def showPopupInvalid(self, bledy):
        showPopup("Błąd walidacji", "Wystąpiły błędy walidacji pliku:\n\n" + bledy)