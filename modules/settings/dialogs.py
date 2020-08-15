# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Settings
 ***************************************************************************/
"""
import os

from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import Qt, QRegExp
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from PyQt5.QtGui import QRegExpValidator


title_settings = 'Ustawienia'
icon_settings = ':/plugins/wtyczka_app/img/ustawienia.png'

# TODO zmienić ikonę helpa
title_help = 'Pomoc'
icon_help = ':/plugins/wtyczka_app/img/ustawienia.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'ustawienia_dialog_base.ui'))

FORM_CLASS1, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'pomoc_dialog_base.ui'))


class UstawieniaDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(UstawieniaDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title_settings)
        self.setWindowIcon(QtGui.QIcon(icon_settings))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        self.exit_btn.clicked.connect(self.reject)
        self.contactMail_lineEdit.setValidator(QRegExpValidator(QRegExp(r"[0-9a-zA-Z.\-\_\@\+]*")))
        self.adminMail_lineEdit.setValidator(QRegExpValidator(QRegExp(r"[0-9a-zA-Z.\-\_\@\+]*")))


class PomocDialog(QtWidgets.QDialog, FORM_CLASS1):
    def __init__(self, parent=None):
        """Constructor."""
        super(PomocDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title_help)
        self.setWindowIcon(QtGui.QIcon(icon_help))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        self.cancel_btn.clicked.connect(self.reject)