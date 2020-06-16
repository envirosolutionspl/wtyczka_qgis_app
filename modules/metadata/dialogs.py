# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Metadata
 ***************************************************************************/
"""

import os

from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import Qt
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from .. import QDialogOverride


title_metadata = 'Tworzenie / aktualizacja metadanych'
icon_metadata = ':/plugins/wtyczka_app/img/tworzenie.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'metadane_dialog_base.ui'))


class MetadaneDialog(QDialogOverride, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(MetadaneDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title_metadata)
        self.setWindowIcon(QtGui.QIcon(icon_metadata))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)

    def closeEvent(self, event):
        if self.sender() is None:
            reply = QMessageBox.question(self, 'Opuszczanie wtyczki APP',
                                         "Jesteś pewien, że chcesz opuścić wtyczkę?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()