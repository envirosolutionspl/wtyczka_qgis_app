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
        self.walidacjaDialog.prev_btn.clicked.connect(self.walidacjaDialog_prev_btn_clicked)

        self.walidacjaDialog.close_btn.setEnabled(False)
        self.walidacjaDialog.export_btn.clicked.connect(self.showPopupExport)
        self.walidacjaDialog.validate_btn.clicked.connect(self.walidacjaDialog_validate_btn_clicked)
        self.walidacjaDialog.validateGML_checkBox.stateChanged.connect(self.gml_checkBoxChangedAction)
        self.walidacjaDialog.validateXML_checkBox.stateChanged.connect(self.xml_checkBoxChangedAction)
        self.walidacjaDialog.close_btn.clicked.connect(self.walidacjaDialog.close)

        self.walidacjaDialog.chooseXML_widget.setFilter("*.xml")
        self.walidacjaDialog.chooseGML_widget.setFilter("*.gml")
        # endregion

    """Event handlers"""
    # region walidacjaDialog
    def walidacjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def walidacjaDialog_validate_btn_clicked(self):
        self.showPopupValidate()
        self.walidacjaDialog.close_btn.setEnabled(True)

    def xml_checkBoxChangedAction(self, state):
        if Qt.Checked == state:
            self.walidacjaDialog.chooseXML_widget.setEnabled(True)
        else:
            self.walidacjaDialog.chooseXML_widget.setEnabled(False)

    def gml_checkBoxChangedAction(self, state):
        if Qt.Checked == state:
            self.walidacjaDialog.chooseGML_widget.setEnabled(True)
        else:
            self.walidacjaDialog.chooseGML_widget.setEnabled(False)
    # endregion

    """Helper methods"""

    """Popup windows"""
    def showPopupExport(self):
        showPopup("Wyeksportuj plik z błędami", "Poprawnie wyeksportowano plik z błędami.")

    def showPopupValidate(self):
        showPopup("Waliduj pliki", "Poprawnie zwalidowano wszystkie wgrane pliki.")