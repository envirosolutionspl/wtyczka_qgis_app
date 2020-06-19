from PyQt5.QtWidgets import QMessageBox

from qgis.PyQt import QtWidgets
from .base import BaseModule
from .Formularz import Formularz


class QDialogOverride(QtWidgets.QDialog):
    def closeEvent(self, event):
        if self.sender() is None:
            reply = QMessageBox.question(self, 'Opuszczanie wtyczki APP',
                                         "Jesteś pewien, że chcesz opuścić wtyczkę?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
