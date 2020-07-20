from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from qgis.PyQt import QtWidgets
from .base import BaseModule
from .Formularz import Formularz
from .settings.dialogs import UstawieniaDialog,PomocDialog

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
class ButtonsDialog:
    def __init__(self):
        vLayout = self.layout().itemAt(0)

        hbox = QHBoxLayout()
        hbox.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        settings_btn = QPushButton()
        settings_btn.setIcon(QIcon(':/plugins/wtyczka_app/img/ustawienia.png'))
        settings_btn.setIconSize(QSize(20, 20))
        settings_btn.setObjectName("settings_btn")
        settings_btn.setToolTip("Ustawienia")
        settings_btn.clicked.connect(self.__settings_btn_clicked)
        hbox.addWidget(settings_btn)
        help_btn = QPushButton()
        help_btn.setIcon(QIcon(':/plugins/wtyczka_app/img/info2.png'))
        help_btn.setIconSize(QSize(20, 20))
        help_btn.setObjectName("help_btn")
        help_btn.setToolTip("Pomoc")
        help_btn.clicked.connect(self.__help_btn_clicked)
        hbox.addWidget(help_btn)
        vLayout.insertLayout(0, hbox)

    def __settings_btn_clicked(self):
        self.ustawieniaDialog = UstawieniaDialog()
        self.ustawieniaDialog.exec()

    def __help_btn_clicked(self):
        self.pomocDialog = PomocDialog()
        self.pomocDialog.exec()