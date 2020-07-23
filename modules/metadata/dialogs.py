# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Metadata
 ***************************************************************************/
"""

import os

from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import Qt, QVariant
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from .. import QDialogOverride, ButtonsDialog, utils


title_metadata = 'Tworzenie / aktualizacja metadanych'
icon_metadata = ':/plugins/wtyczka_app/img/tworzenie.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'metadane_dialog_base.ui'))


class MetadaneDialog(QDialogOverride, FORM_CLASS, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(MetadaneDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title_metadata)
        self.setWindowIcon(QtGui.QIcon(icon_metadata))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        ButtonsDialog.__init__(self)
        self.prepareLayout()

    def prepareLayout(self):
        """Przygotowanie layoutu metadanych"""
        for listWidget in utils.getWidgetsByType(self, QListWidget):
            self.prepareListWidgets(listWidget)

    def prepareListWidgets(self, listWidget):
        """Przygotowanie obsługi pól wielokrotnej liczności"""
        def clearDataFromListWidget():
            for input in inputs:
                if isinstance(input,QComboBox):
                    input.setCurrentIndex(0)
                if isinstance(input, QLineEdit):
                    input.clear()
                if isinstance(input, QDateTimeEdit):
                    input.clear()

        def checkValidity():
            if elementId == 'e22' or elementId == 'e29':
                if nameLineEdit.text() and mailLineEdit.text():
                    return True
            if lineEdit and lineEdit.text():
                return True
            return False
        def getDataFromListWidget(listItem):
            data = listItem.data(Qt.UserRole)
            for input in inputs:
                if isinstance(input,QLineEdit):
                    input.setText(data[input.objectName()])
                elif isinstance(input,QDateTimeEdit):
                    input.setDate(data[input.objectName()])
                elif isinstance(input,QComboBox):
                    input.setCurrentIndex(data[input.objectName()])
        def addItem():
            print("ADD")
            if checkValidity():  # jeżeli pola są wypełnione
                newItem = QListWidgetItem()
                data = {}
                textList = []
                for input in inputs:
                    if input:
                        if isinstance(input, QLineEdit):
                            data[input.objectName()] = input.text()
                            textList.append(input.text())
                        if isinstance(input, QComboBox):
                            data[input.objectName()] = input.currentIndex()
                            textList.append(input.currentText())
                        if isinstance(input, QDateTimeEdit):
                            data[input.objectName()] = input.dateTime()
                            textList.append(input.dateTime().toString())
                newItem.setData(Qt.UserRole,QVariant(data))
                newItem.setText(" - ".join(textList))
                listWidget.addItem(newItem)
                clearDataFromListWidget()  # czyszczenie
            else:
                utils.showPopup("Wypełnij formularz mapy podkładowej",
                                'Musisz zdefiniować wartości dla wszystkich pól')
        def removeItem(listWidget):
            listWidget.takeItem(listWidget.currentRow())

        # print(listWidget.objectName())
        elementId = listWidget.objectName().split('_')[0]
        add_btn = utils.getWidgetByName(self, QPushButton, elementId + "_add_btn")
        remove_btn = utils.getWidgetByName(self, QPushButton, elementId + "_remove_btn")
        lineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_lineEdit")
        mailLineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_mail_lineEdit")
        nameLineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_name_lineEdit")
        dateTimeEdit = utils.getWidgetByName(self, QDateTimeEdit, elementId + "_dateTimeEdit")
        cmbbx = utils.getWidgetByName(self, QComboBox, elementId + "_cmbbx")

        inputs = [lineEdit, dateTimeEdit, cmbbx, mailLineEdit, nameLineEdit]
        add_btn.clicked.connect(addItem)
        remove_btn.clicked.connect(lambda: removeItem(listWidget))
        listWidget.itemDoubleClicked.connect(getDataFromListWidget)

