from . import (UstawieniaDialog, PomocDialog, ustawieniaDialog, PLUGIN_VERSION)
from .. import BaseModule
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
        self.settingsSmtpDialog = SmtpDialog(self.iface)
        self.settingsCswDialog = CswDialog(self.iface)
        # region okno moduł help
        self.pomocDialog = PomocDialog()
        # print('kkkkk', PLUGIN_VERSION)

        # endregion

        self.readSettings()

        self.ustawieniaDialog.folder_btn.clicked.connect(self.folder_btn_clicked)
        self.ustawieniaDialog.save_btn.clicked.connect(self.save_btn_clicked)
        self.ustawieniaDialog.smtp_btn.clicked.connect(self.smtp_btn_clicked)
        self.ustawieniaDialog.csw_btn.clicked.connect(self.csw_btn_clicked)

    """Event handlers"""
    def folder_btn_clicked(self):
        path = QFileDialog.getExistingDirectory(self.ustawieniaDialog, "Wskaż domyślny folder zapisu", "/", QFileDialog.ShowDirsOnly)
        if path:
            self.ustawieniaDialog.folder_lbl.setText(path)

    def save_btn_clicked(self):
        s = QgsSettings()
        s.setValue("qgis_app/settings/defaultPath", self.ustawieniaDialog.folder_lbl.text())
        s.setValue("qgis_app/settings/contactName", self.ustawieniaDialog.contactName_lineEdit.text())
        s.setValue("qgis_app/settings/contactMail", self.ustawieniaDialog.contactMail_lineEdit.text())
        s.setValue("qgis_app/settings/adminName", self.ustawieniaDialog.adminName_lineEdit.text())
        s.setValue("qgis_app/settings/adminMail", self.ustawieniaDialog.adminMail_lineEdit.text())

    def smtp_btn_clicked(self):
        self.settingsSmtpDialog.show()
        self.settingsSmtpDialog.send_btn.setVisible(False)

    def csw_btn_clicked(self):
        self.settingsCswDialog.show()
        self.settingsCswDialog.send_btn.setVisible(False)

    def readSettings(self):
        s = QgsSettings()
        self.ustawieniaDialog.folder_lbl.setText(s.value("qgis_app/settings/defaultPath", ""))
        self.ustawieniaDialog.contactName_lineEdit.setText(s.value("qgis_app/settings/contactName", ""))
        self.ustawieniaDialog.contactMail_lineEdit.setText(s.value("qgis_app/settings/contactMail", ""))
        self.ustawieniaDialog.adminName_lineEdit.setText(s.value("qgis_app/settings/adminName", ""))
        self.ustawieniaDialog.adminMail_lineEdit.setText(s.value("qgis_app/settings/adminMail", ""))
    """Helper methods"""

    """Popup windows"""
