from . import (MetadaneDialog)
from .. import BaseModule
from ..utils import showPopup

from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtCore import Qt
import os


class MetadataModule(BaseModule):
    walidacjaDialog = None

    def __init__(self, iface):
        self.iface = iface

        # region okno moduł metadata
        self.metadaneDialog = MetadaneDialog()
        # endregion

        # region eventy moduł metadata
        self.metadaneDialog.prev_btn.clicked.connect(self.metadaneDialog_prev_btn_clicked)
        self.metadaneDialog.next_btn.clicked.connect(self.metadaneDialog_next_btn_clicked)

        self.metadaneDialog.validateAndSave_btn.clicked.connect(self.showPopupValidateAndSave)

        self.metadaneDialog.newMetadata_radioButton.toggled.connect(self.newMetadataRadioButton_toggled)
        self.metadaneDialog.existingMetadata_radioButton.toggled.connect(self.existingMetadataRadioButton_toggled)

        self.metadaneDialog.newFile_widget.clicked.connect(self.saveMetaFile)
        self.metadaneDialog.chooseFile_widget.clicked.connect(self.openMetaFile)
        # endregion

    """Event handlers"""
    # region metadaneDialog
    def metadaneDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def metadaneDialog_next_btn_clicked(self):
        self.openNewDialog(self.walidacjaDialog)
        self.listaOkienek.append(self.metadaneDialog)
        self.walidacjaDialog.prev_btn.setEnabled(True)

    def newMetadataRadioButton_toggled(self, enabled):
        if enabled:
            self.metadaneDialog.newFile_widget.setEnabled(True)
            self.metadaneDialog.chooseFile_widget.setEnabled(False)
            self.metadaneDialog.file_lbl.setText("...")

    def existingMetadataRadioButton_toggled(self, enabled):
        if enabled:
            self.metadaneDialog.newFile_widget.setEnabled(False)
            self.metadaneDialog.chooseFile_widget.setEnabled(True)
            self.metadaneDialog.file_lbl.setText("...")

    def server_checkBoxChangedAction(self, state):
        if Qt.Checked == state:
            self.metadaneDialog.send_btn.setEnabled(True)
        else:
            if self.metadaneDialog.email_checkBox.isChecked():
                self.metadaneDialog.send_btn.setEnabled(True)
            else:
                self.metadaneDialog.send_btn.setEnabled(False)

    def email_checkBoxChangedAction(self, state):
        if Qt.Checked == state:
            self.metadaneDialog.send_btn.setEnabled(True)
        else:
            if self.metadaneDialog.server_checkBox.isChecked():
                self.metadaneDialog.send_btn.setEnabled(True)
            else:
                self.metadaneDialog.send_btn.setEnabled(False)
    # endregion

    """Helper methods"""
    def saveMetaFile(self):
        self.outputPlik = QFileDialog.getSaveFileName(filter="*.xml")[0]
        if self.outputPlik != '':
            self.metadaneDialog.file_lbl.setText(self.outputPlik)

    def openMetaFile(self):
        self.plik = QFileDialog.getOpenFileName(filter="*.xml")[0]
        if self.plik != '':
            self.metadaneDialog.file_lbl.setText(self.plik)

    """Popup windows"""
    def showPopupValidateAndSave(self):
        showPopup("Zwaliduj i zapisz plik XML", "Poprawnie zwalidowano oraz zapisano plik XML.")

    def showPopupSend(self):
        showPopup("Wyśli plik", "Wysłano plik XML zawierający metadane.")