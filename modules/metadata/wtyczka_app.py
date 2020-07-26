from . import (MetadaneDialog, SmtpDialog, CswDialog)
from .metadata_form_validator import validateMetadataForm
from .metadata_import_eksport import formToMetadataElementList
from .. import BaseModule
from ..utils import showPopup
from .. import utils
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import os


class MetadataModule(BaseModule):
    walidacjaDialog = None

    def __init__(self, iface):
        self.iface = iface

        self.saved = False
        # plik metadanych do wysłania
        # TODO: Zmienić self.metadataXmlPath na ścieżkę pliku do wysłania
        self.metadataXmlPath = os.path.join(os.path.dirname(__file__), '../validator', 'test_metadata.xml')
        # region okno moduł metadata
        self.metadaneDialog = MetadaneDialog()
        # endregion
        self.smtpDialog = SmtpDialog(iface=self.iface)
        self.cswDialog = CswDialog(iface=self.iface)

        # region eventy moduł metadata
        self.metadaneDialog.prev_btn.clicked.connect(self.metadaneDialog_prev_btn_clicked)
        self.metadaneDialog.validateAndSave_btn.clicked.connect(self.showPopupValidateAndSave)
        self.metadaneDialog.close_btn.clicked.connect(self.metadaneDialog.close)

        self.metadaneDialog.email_btn.clicked.connect(self.metadaneDialog_email_btn_clicked)
        self.metadaneDialog.server_btn.clicked.connect(self.metadaneDialog_server_btn_clicked)

        # self.metadaneDialog.newFile_widget.clicked.connect(self.saveMetaFile)
        self.metadaneDialog.chooseFile_widget.setFilter("*.xml")
        self.metadaneDialog.chooseSet_widget.setFilter("*.gml")
        # endregion

    """Event handlers"""
    # region metadaneDialog
    def metadaneDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())
        self.metadaneDialog.server_btn.setEnabled(False)
        self.metadaneDialog.email_btn.setEnabled(False)

    def metadaneDialog_next_btn_clicked(self):
        self.openNewDialog(self.walidacjaDialog)
        self.listaOkienek.append(self.metadaneDialog)
        self.walidacjaDialog.prev_btn.setEnabled(True)

    def metadaneDialog_email_btn_clicked(self):
        self.smtpDialog.setXmlPath(self.metadataXmlPath)
        self.smtpDialog.show()

    def metadaneDialog_server_btn_clicked(self):
        self.cswDialog.setXmlPath(self.metadataXmlPath)
        self.cswDialog.show()

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
    # def saveMetaFile(self):
    #     self.outputPlik = QFileDialog.getSaveFileName(filter="*.xml")[0]
    #     if self.outputPlik != '':
    #         self.metadaneDialog.file_lbl.setText(self.outputPlik)

    # def openMetaFile(self):
    #     self.plik = QFileDialog.getOpenFileName(filter="*.xml")[0]
    #     if self.plik != '':
    #         self.metadaneDialog.file_lbl.setText(self.plik)

    """Popup windows"""
    def showPopupValidateAndSave(self):
        formToMetadataElementList(self.metadaneDialog)
        validationResult = validateMetadataForm(dlg=self.metadaneDialog)
        if validationResult[0]:
            showPopup("Zwaliduj i zapisz plik XML", "Poprawnie zwalidowano oraz zapisano plik XML.")
            self.metadaneDialog.server_btn.setEnabled(True)
            self.metadaneDialog.email_btn.setEnabled(True)
        else:
            msg = validationResult[1]
            utils.showPopup("Błąd walidacji formularza", msg, QMessageBox.Warning)