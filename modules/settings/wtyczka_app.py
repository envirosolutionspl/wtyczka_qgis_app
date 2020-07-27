from . import (UstawieniaDialog, PomocDialog)
from .. import BaseModule
from . import ustawieniaDialog
from ..utils import showPopup
from ..metadata import SmtpDialog, CswDialog

from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtCore import Qt
from qgis.core import QgsSettings
import os


class SettingsModule(BaseModule):

    def __init__(self, iface):
        self.iface = iface

        # region okno moduł settings
        self.ustawieniaDialog = ustawieniaDialog
        # endregion

        # region okno moduł help
        self.pomocDialog = PomocDialog()
        # endregion

        self.readSettings()

        self.ustawieniaDialog.folder_btn.clicked.connect(self.folder_btn_clicked)
        self.ustawieniaDialog.save_btn.clicked.connect(self.save_btn_clicked)
        self.ustawieniaDialog.smtp_btn.clicked.connect(self.smtp_btn_clicked)
        self.ustawieniaDialog.csw_btn.clicked.connect(self.csw_btn_clicked)

    """Event handlers"""
    def folder_btn_clicked(self):
        path = QFileDialog.getExistingDirectory(self.ustawieniaDialog, "Open Directory", "/", QFileDialog.ShowDirsOnly)
        if path:
            self.ustawieniaDialog.folder_lbl.setText(path)

    def save_btn_clicked(self):
        s = QgsSettings()
        s.setValue("qgis_app/settings/defaultPath", self.ustawieniaDialog.folder_lbl.text())
        s.setValue("qgis_app/settings/contactName", self.ustawieniaDialog.name_lineEdit.text())
        s.setValue("qgis_app/settings/contactMail", self.ustawieniaDialog.mail_lineEdit.text())

    def smtp_btn_clicked(self):
        smtpDialog = SmtpDialog(self.iface)
        smtpDialog.show()
        smtpDialog.send_btn.setVisible(False)

    def csw_btn_clicked(self):
        cswDialog = CswDialog(self.iface)
        cswDialog.show()
        cswDialog.send_btn.setVisible(False)

    def readSettings(self):
        s = QgsSettings()
        self.ustawieniaDialog.folder_lbl.setText(s.value("qgis_app/settings/defaultPath", ""))
        self.ustawieniaDialog.name_lineEdit.setText(s.value("qgis_app/settings/contactName", ""))
        self.ustawieniaDialog.mail_lineEdit.setText(s.value("qgis_app/settings/contactMail", ""))

    """Helper methods"""

    """Popup windows"""
