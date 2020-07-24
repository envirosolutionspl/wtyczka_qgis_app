from . import (MetadaneDialog, SmtpDialog)

from .. import BaseModule
from ..utils import showPopup
from .. import utils
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import os


class MetadataModule(BaseModule):
    walidacjaDialog = None

    def __init__(self, iface):
        self.iface = iface

        self.saved = False
        #plik metadanych do wysłania
        self.metadataXmlPath = os.path.join(os.path.dirname(__file__),'../validator','appExample_pzpw_v001.xml')
        # region okno moduł metadata
        self.metadaneDialog = MetadaneDialog()
        # endregion
        self.smtpDialog = SmtpDialog(iface=self.iface)


        # region eventy moduł metadata
        self.metadaneDialog.prev_btn.clicked.connect(self.metadaneDialog_prev_btn_clicked)
        self.metadaneDialog.validateAndSave_btn.clicked.connect(self.showPopupValidateAndSave)
        self.metadaneDialog.close_btn.clicked.connect(self.metadaneDialog.close)

        self.metadaneDialog.email_btn.clicked.connect(self.metadaneDialog_email_btn_clicked)
        #self.metadaneDialog.newMetadata_radioButton.toggled.connect(self.newMetadataRadioButton_toggled)
        #self.metadaneDialog.existingMetadata_radioButton.toggled.connect(self.existingMetadataRadioButton_toggled)

        # self.metadaneDialog.newFile_widget.clicked.connect(self.saveMetaFile)
        self.metadaneDialog.chooseFile_widget.clicked.connect(self.openMetaFile)
        self.metadaneDialog.chooseSet_widget.setFilter("*.gml")
        # endregion
        self.prepareLayout()

    def prepareLayout(self):
        p = QPixmap(':/plugins/wtyczka_app/img/info1.png')

        # nadanie grafiki tooltipa
        for label in utils.getWidgetsByType(self.metadaneDialog, QLabel):
            # print(label.objectName())
            if label.objectName().endswith("_tooltip"):
                label.setMaximumWidth(16)
                label.setPixmap(p.scaled(16, 16, Qt.KeepAspectRatio))

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




    # def newMetadataRadioButton_toggled(self, enabled):
    #     if enabled:
    #         self.metadaneDialog.newFile_widget.setEnabled(True)
    #         self.metadaneDialog.chooseFile_widget.setEnabled(False)
    #         self.metadaneDialog.file_lbl.setText("...")
    #
    # def existingMetadataRadioButton_toggled(self, enabled):
    #     if enabled:
    #         self.metadaneDialog.newFile_widget.setEnabled(False)
    #         self.metadaneDialog.chooseFile_widget.setEnabled(True)
    #         self.metadaneDialog.file_lbl.setText("...")

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

    def openMetaFile(self):
        self.plik = QFileDialog.getOpenFileName(filter="*.xml")[0]
        if self.plik != '':
            self.metadaneDialog.file_lbl.setText(self.plik)

    """Popup windows"""
    def showPopupValidateAndSave(self):
        showPopup("Zwaliduj i zapisz plik XML", "Poprawnie zwalidowano oraz zapisano plik XML.")
        self.metadaneDialog.server_btn.setEnabled(True)
        self.metadaneDialog.email_btn.setEnabled(True)

    def showPopupSend(self):
        showPopup("Wyślij plik", "Wysłano plik XML zawierający metadane.")