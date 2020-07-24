# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Metadata
 ***************************************************************************/
"""

import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QRegExpValidator
from qgis.PyQt.QtCore import Qt, QVariant, QRegExp
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from qgis.core import QgsSettings
from qgis.gui import QgisInterface
from .. import QDialogOverride, ButtonsDialog, utils
from . import mail


title_metadata = 'Tworzenie / aktualizacja metadanych'
icon_metadata = ':/plugins/wtyczka_app/img/tworzenie.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'metadane_dialog_base.ui'))
FORM_CLASS2, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'smtp_dlg.ui'))
class SmtpDialog(QtWidgets.QDialog, FORM_CLASS2):
    def __init__(self, iface, xmlPath=None, parent=None,):
        """Constructor."""
        super(SmtpDialog, self).__init__(parent)
        self.iface = iface
        self.xmlPath = xmlPath
        self.setupUi(self)
        # self.setWindowTitle(title_metadata)
        self.setWindowIcon(QtGui.QIcon(icon_metadata))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        self.prepareLayout()

    def setXmlPath(self, xmlPath):
        self.xmlPath = xmlPath

    def prepareLayout(self):
        """Przygotowanie layoutu SMTP"""

        self.port_lineEdit.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.host_lineEdit.setValidator(QRegExpValidator(QRegExp(r"\S*")))
        self.receiver_lineEdit.setValidator(QRegExpValidator(QRegExp(r"\S*")))
        self.readSettings() # wczytaj zapisane wartości
        self.cancel_btn.clicked.connect(self.close)
        self.send_btn.clicked.connect(self.send_btn_clicked)
        self.save_btn.clicked.connect(self.saveSettings)


    def send_btn_clicked(self):
        result = self.validateForm()
        if result[0]:
            sendResult = mail.sendMail(
                sender=self.user_lineEdit.text(),
                host=self.host_lineEdit.text(),
                port=self.port_lineEdit.text(),
                receiver=self.receiver_lineEdit.text(),
                password=self.pass_lineEdit.text(),
                file=self.xmlPath
            )
            if sendResult[0]:
                self.iface.messageBar().pushSuccess("Mail:","Pomyslnie wysłano plik")
                self.close()
            else:
                self.iface.messageBar().pushCritical("Mail:", "Nie udało się wysłać pliku")
                msg = sendResult[1]
                utils.showPopup("Błąd wysyłki", msg, QMessageBox.Warning)

        else:   #błąd walidacji formularza
            msg = result[1]
            utils.showPopup("Błąd formularza", msg, QMessageBox.Warning)

    def saveSettings(self):
        """Sprawdzanie Chceckboxów do zapisu ustawień"""
        s = QgsSettings()
        for chkbx in utils.getWidgetsByType(self, QCheckBox):
            if chkbx.isChecked():
                elementId = chkbx.objectName().split("_")[0]
                lineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_lineEdit")
                s.setValue("qgis_app/smtp/%s" % elementId, lineEdit.text())

    def readSettings(self):
        """Odczyt zapisu ustawień"""
        s = QgsSettings()
        for lineEdit in utils.getWidgetsByType(self, QLineEdit):
            elementId = lineEdit.objectName().split("_")[0]
            savedValue = s.value("qgis_app/smtp/%s" % elementId, '')
            if savedValue:  # jeżeli była wartość zapisana w ustawieniach
                chkbx = utils.getWidgetByName(self, QCheckBox, elementId + "_chkbx")
                chkbx.setChecked(True)
            lineEdit.setText(savedValue)

    def validateForm(self):
        """walidacja formularza"""
        for lineEdit in utils.getWidgetsByType(self, QLineEdit):
            if not lineEdit.text():
                elementId = lineEdit.objectName().split("_")[0]
                label = utils.getWidgetByName(self, QLabel, elementId + "_lbl")
                return (False, "Musisz wypełnić pole %s" % label.text())
        return [True]






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

