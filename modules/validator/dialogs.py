# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Metadata
 ***************************************************************************/
"""

import os

from PyQt5.QtWidgets import QMessageBox

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets



# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'walidacja_gmlxml_dialog_base.ui'))


class WalidacjaDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(WalidacjaDialog, self).__init__(parent)
        self.setupUi(self)

    def closeEvent(self, event):
        if self.sender() is None:
            reply = QMessageBox.question(self, 'Opuszczanie wtyczki APP',
                                         "Jesteś pewien, że chcesz opuścić wtyczkę?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()