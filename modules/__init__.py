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
    ustawieniaDialog = UstawieniaDialog()
    pomocDialog = PomocDialog()

    def __init__(self):
        vLayout = self.layout().itemAt(0)


        hbox = QHBoxLayout()
        hbox.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(QIcon(':/plugins/wtyczka_app/img/ustawienia.png'))
        self.settings_btn.setIconSize(QSize(20, 20))
        self.settings_btn.setObjectName("settings_btn")
        self.settings_btn.setToolTip("Ustawienia")
        self.settings_btn.setAutoDefault(False)
        self.settings_btn.clicked.connect(self.settings_btn_clicked)
        hbox.addWidget(self.settings_btn)
        self.help_btn = QPushButton()
        self.help_btn.setIcon(QIcon(':/plugins/wtyczka_app/img/info2.png'))
        self.help_btn.setIconSize(QSize(20, 20))
        self.help_btn.setObjectName("help_btn")
        self.help_btn.setToolTip("Pomoc")
        self.help_btn.setAutoDefault(False)
        self.help_btn.clicked.connect(self.help_btn_clicked)
        hbox.addWidget(self.help_btn)
        vLayout.insertLayout(0, hbox)

    def settings_btn_clicked(self):
        self.ustawieniaDialog.exec()

    def help_btn_clicked(self):
        self.pomocDialog.exec()