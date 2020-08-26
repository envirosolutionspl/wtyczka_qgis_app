# -*- coding: utf-8 -*-
from . import (UstawieniaDialog, PomocDialog, ustawieniaDialog, PLUGIN_VERSION)
from .. import BaseModule, dictionaries
from ..utils import showPopup, getWidgetByName, settingsValidateDatasetId
from ..metadata import SmtpDialog, CswDialog
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtCore import Qt, QVariant, QRegExp
from qgis.core import QgsSettings
import os
from PyQt5.QtGui import *
from qgis.PyQt.QtCore import Qt, QVariant, QRegExp, QDateTime


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
        self.set_field_validators()
        self.add_rodzajZbioru_values()
        self.readSettings()

        self.preparePrzestrzenNazw()

        self.ustawieniaDialog.folder_btn.clicked.connect(
            self.folder_btn_clicked)
        self.ustawieniaDialog.save_btn.clicked.connect(self.validate_settings)
        self.ustawieniaDialog.smtp_btn.clicked.connect(self.smtp_btn_clicked)
        self.ustawieniaDialog.csw_btn.clicked.connect(self.csw_btn_clicked)

    """Event handlers"""

    def set_field_validators(self):
        self.ustawieniaDialog.numerZbioru_lineEdit.setValidator(
            QRegExpValidator(QRegExp("[0-9]*")))
        self.ustawieniaDialog.jpt_lineEdit.setValidator(
            QRegExpValidator(QRegExp("[0-9]*")))

    def add_rodzajZbioru_values(self):
        values = dictionaries.rodzajeZbiorow.keys()
        self.ustawieniaDialog.rodzajZbioru_comboBox.addItems(values)

    def folder_btn_clicked(self):
        path = QFileDialog.getExistingDirectory(
            self.ustawieniaDialog, "Wskaż domyślny folder zapisu", "/", QFileDialog.ShowDirsOnly)
        if path:
            self.ustawieniaDialog.folder_lbl.setText(path)

    def validate_settings(self):

        if settingsValidateDatasetId(self.ustawieniaDialog.przestrzenNazw_lineEdit.text()):
            self.save_btn_clicked()
            showPopup('Ustawienia', 'Ustawienia zostały zapisane.\n\nWyłącz i włącz program QGIS lub użyj wtyczki "Plugin Reloader" w celu zastosowania zmian.')
        else:
            showPopup(
                'Ustawienia', 'Ustawienia nie zostały zapisane.\nBłędna wartość dla pola przestrzenNazw.')

    def save_btn_clicked(self):
        s = QgsSettings()
        s.setValue("qgis_app/settings/defaultPath",
                   self.ustawieniaDialog.folder_lbl.text())
        s.setValue("qgis_app/settings/contactName",
                   self.ustawieniaDialog.contactName_lineEdit.text())
        s.setValue("qgis_app/settings/contactMail",
                   self.ustawieniaDialog.contactMail_lineEdit.text())
        s.setValue("qgis_app/settings/adminName",
                   self.ustawieniaDialog.adminName_lineEdit.text())
        s.setValue("qgis_app/settings/adminMail",
                   self.ustawieniaDialog.adminMail_lineEdit.text())
        s.setValue("qgis_app/settings/przestrzenNazw",
                   self.ustawieniaDialog.przestrzenNazw_lineEdit.text())
        s.setValue("qgis_app/settings/numerZbioru",
                   self.ustawieniaDialog.numerZbioru_lineEdit.text())
        s.setValue("qgis_app/settings/jpt",
                   self.ustawieniaDialog.jpt_lineEdit.text())
        s.setValue("qgis_app/settings/rodzajZbioru",
                   self.ustawieniaDialog.rodzajZbioru_comboBox.currentText())  # COMBOBOX

    def preparePrzestrzenNazw(self):
        def updatePrzestrzenNazw():
            przestrzenNazw_list = []
            przestrzenNazw_lineEdit = self.ustawieniaDialog.przestrzenNazw_lineEdit
            numerZbioru_lineEdit = self.ustawieniaDialog.numerZbioru_lineEdit.text()
            jpt_lineEdit = self.ustawieniaDialog.jpt_lineEdit.text()
            rodzajZbioru_comboBox = self.ustawieniaDialog.rodzajZbioru_comboBox.currentText()
            if numerZbioru_lineEdit.strip():
                przestrzenNazw_list.append(numerZbioru_lineEdit.strip()+'/')
            if jpt_lineEdit.strip():
                przestrzenNazw_list.append(jpt_lineEdit.strip())
            if rodzajZbioru_comboBox.strip():
                przestrzenNazw_list.append('-'+rodzajZbioru_comboBox.strip())
            przestrzenNazw_lineEdit.setText(
                'PL.ZIPPZP.'+"".join(przestrzenNazw_list))

        # pobranie dynamicznie utworzonych obiektów UI
        przestrzenNazw_lineEdit = self.ustawieniaDialog.przestrzenNazw_lineEdit
        numerZbioru_lineEdit = self.ustawieniaDialog.numerZbioru_lineEdit
        jpt_lineEdit = self.ustawieniaDialog.jpt_lineEdit
        rodzajZbioru_comboBox = self.ustawieniaDialog.rodzajZbioru_comboBox

        # definicja Eventów dynamicznych obiektów UI
        numerZbioru_lineEdit.textChanged.connect(
            lambda: updatePrzestrzenNazw())
        jpt_lineEdit.textChanged.connect(
            lambda: updatePrzestrzenNazw())
        rodzajZbioru_comboBox.currentTextChanged.connect(
            lambda: updatePrzestrzenNazw())

    def smtp_btn_clicked(self):
        self.settingsSmtpDialog.show()
        self.settingsSmtpDialog.send_btn.setVisible(False)

    def csw_btn_clicked(self):
        self.settingsCswDialog.show()
        self.settingsCswDialog.send_btn.setVisible(False)

    def readSettings(self):
        s = QgsSettings()
        self.ustawieniaDialog.folder_lbl.setText(
            s.value("qgis_app/settings/defaultPath", ""))
        self.ustawieniaDialog.contactName_lineEdit.setText(
            s.value("qgis_app/settings/contactName", ""))
        self.ustawieniaDialog.contactMail_lineEdit.setText(
            s.value("qgis_app/settings/contactMail", ""))
        self.ustawieniaDialog.adminName_lineEdit.setText(
            s.value("qgis_app/settings/adminName", ""))
        self.ustawieniaDialog.adminMail_lineEdit.setText(
            s.value("qgis_app/settings/adminMail", ""))
        self.ustawieniaDialog.przestrzenNazw_lineEdit.setText(
            s.value("qgis_app/settings/przestrzenNazw", "PL.ZIPPZP."))
        self.ustawieniaDialog.numerZbioru_lineEdit.setText(
            s.value("qgis_app/settings/numerZbioru", ""))
        self.ustawieniaDialog.jpt_lineEdit.setText(
            s.value("qgis_app/settings/jpt", ""))
        self.ustawieniaDialog.rodzajZbioru_comboBox.setCurrentIndex(
            list(dictionaries.rodzajeZbiorow.keys()).index(s.value("qgis_app/settings/rodzajZbioru", "")))
    """Helper methods"""

    """Popup windows"""
