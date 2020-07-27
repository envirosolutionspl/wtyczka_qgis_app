# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Metadata
 ***************************************************************************/
"""

import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qgis.PyQt.QtCore import Qt, QVariant, QRegExp
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from qgis.core import QgsSettings
from qgis.gui import QgisInterface
from .. import QDialogOverride, ButtonsDialog, utils, dictionaries
from . import mail, csw


title_metadata = 'Tworzenie / aktualizacja metadanych'
icon_metadata = ':/plugins/wtyczka_app/img/tworzenie.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'metadane_dialog_base.ui'))
FORM_CLASS2, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'smtp_dlg.ui'))
FORM_CLASS3, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'csw_dlg.ui'))


class SendFileDialog:
    """klasa bazowa dla formularzy wysyłki pliku metadanych"""

    def setXmlPath(self, xmlPath):
        self.xmlPath = xmlPath

    def saveSettings(self, formName):
        """Sprawdzanie Chceckboxów do zapisu ustawień"""
        s = QgsSettings()
        checked = False
        for chkbx in utils.getWidgetsByType(self, QCheckBox):
            if chkbx.isChecked():
                elementId = chkbx.objectName().split("_")[0]
                lineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_lineEdit")
                s.setValue("qgis_app/%s/%s" % (formName, elementId), lineEdit.text())
                checked = True
        if checked:
            self.iface.messageBar().pushSuccess("Zapis parametrów połączenia:", "Pomyslnie zapisano wskazane parametry połączenia")


    def readSettings(self, formName):
        """Odczyt zapisu ustawień"""
        s = QgsSettings()
        for lineEdit in utils.getWidgetsByType(self, QLineEdit):
            elementId = lineEdit.objectName().split("_")[0]
            savedValue = s.value("qgis_app/%s/%s" % (formName, elementId), '')
            if savedValue:  # jeżeli była wartość zapisana w ustawieniach
                chkbx = utils.getWidgetByName(self, QCheckBox, elementId + "_chkbx")
                chkbx.setChecked(True)
            lineEdit.setText(savedValue)

    def validateForm(self):
        """walidacja formularza"""
        for lineEdit in utils.getWidgetsByType(self, QLineEdit):
            if not lineEdit.text().strip():
                elementId = lineEdit.objectName().split("_")[0]
                label = utils.getWidgetByName(self, QLabel, elementId + "_lbl")
                return (False, "Musisz wypełnić pole %s" % label.text())
        return [True]


class CswDialog(QtWidgets.QDialog, FORM_CLASS3, SendFileDialog):
    """Okno dialogowe formularza CSW"""
    def __init__(self, iface, xmlPath=None, parent=None,):
        """Constructor."""
        super(CswDialog, self).__init__(parent)
        self.send_btn = None
        self.save_btn = None
        self.iface = iface
        self.xmlPath = xmlPath
        self.setupUi(self)
        # self.setWindowTitle(title_metadata)
        self.setWindowIcon(QtGui.QIcon(icon_metadata))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        self.prepareLayout()

    def prepareLayout(self):
        """Przygotowanie layoutu CSW"""

        self.host_lineEdit.setValidator(QRegExpValidator(QRegExp(r"\S*")))
        self.readSettings("csw")  # wczytaj zapisane wartości
        self.cancel_btn.clicked.connect(self.close)
        self.send_btn.clicked.connect(self.send_btn_clicked)
        self.save_btn.clicked.connect(lambda: self.saveSettings("csw"))

    def send_btn_clicked(self):
        result = self.validateForm()
        if result[0]:
            sendResult = csw.putFileToCswServer(
                url=self.host_lineEdit.text(),
                user=self.user_lineEdit.text(),
                password=self.pass_lineEdit.text(),
                file=self.xmlPath
            )
            if sendResult[0]:
                self.iface.messageBar().pushSuccess("CSW:","Pomyslnie wysłano plik")
                self.close()
            else:
                self.iface.messageBar().pushCritical("CSW:", "Nie udało się wysłać pliku")
                msg = sendResult[1]
                utils.showPopup("Błąd wysyłki", msg, QMessageBox.Warning)

        else:   #błąd walidacji formularza
            msg = result[1]
            utils.showPopup("Błąd formularza", msg, QMessageBox.Warning)


class SmtpDialog(QtWidgets.QDialog, FORM_CLASS2, SendFileDialog):
    """Okno dialogowe formularza SMTP"""
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

    def prepareLayout(self):
        """Przygotowanie layoutu SMTP"""

        self.port_lineEdit.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.host_lineEdit.setValidator(QRegExpValidator(QRegExp(r"\S*")))
        self.receiver_lineEdit.setValidator(QRegExpValidator(QRegExp(r"\S*")))
        self.readSettings("smtp")   # wczytaj zapisane wartości
        self.cancel_btn.clicked.connect(self.close)
        self.send_btn.clicked.connect(self.send_btn_clicked)
        self.save_btn.clicked.connect(lambda: self.saveSettings("smtp"))

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

        p = QPixmap(':/plugins/wtyczka_app/img/info1.png')

        # Ograniczenia Pól
        input = utils.getWidgetByName(self, QLineEdit, "e11_lineEdit")
        input.setValidator(QRegExpValidator(QRegExp("[0-9.,]*")))
        input = utils.getWidgetByName(self, QLineEdit, "e16_lineEdit")
        input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))


        # nadanie grafiki tooltipa
        for label in utils.getWidgetsByType(self, QLabel):
            # print(label.objectName())
            if label.objectName().endswith("_tooltip"):
                label.setMaximumWidth(16)
                label.setPixmap(p.scaled(16, 16, Qt.KeepAspectRatio))

                label.setToolTip(
                    "<FONT COLOR=black>%s</FONT>" % label.toolTip())  # dodanie tooltip z documentation 'rich text' dla zawijania

    def prepareListWidgets(self, listWidget):
        """Przygotowanie obsługi pól wielokrotnej liczności"""
        def clearDataFromListWidget():
            if elementId == 'e22':
                utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e23_cmbbx').setCurrentIndex(0)
            if elementId == 'e18':
                utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e19_cmbbx').setCurrentIndex(0)
            if elementId == 'e24':
                utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e25_lineEdit').clear()
            if elementId == 'e9':
                utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e10_lineEdit').clear()
                utils.getWidgetByName(layout=self, searchObjectType=QDateTimeEdit, name='e10_dateTimeEdit').clear()
                utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e10_cmbbx').setCurrentIndex(0)
            for input in inputs:
                if isinstance(input, QComboBox):
                    input.setCurrentIndex(0)
                if isinstance(input, QLineEdit):
                    input.clear()
                if isinstance(input, QDateTimeEdit):
                    input.clear()

        def checkValidity():
            """sprawdzenie poprawności pól przed dodaniem do listWidget"""
            if elementId == 'e22' or elementId == 'e29':
                if nameLineEdit.text() and mailLineEdit.text():
                    return True
            elif elementId == 'e7' or elementId == 'e12':
                if cmbbx.currentText():
                    return True
            elif elementId == 'e24':
                if lineEdit.text() and utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e25_lineEdit').text():
                    return True
            elif elementId == 'e9':
                if (
                        lineEdit.text() and
                        utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e10_lineEdit').text() and
                        utils.getWidgetByName(layout=self, searchObjectType=QDateTimeEdit, name='e10_dateTimeEdit').dateTime()):
                    return True
            elif lineEdit and lineEdit.text():
                return True
            return False

        def getDataFromListWidget(listItem):
            data = listItem.data(Qt.UserRole)
            for input in inputs:
                if isinstance(input, QLineEdit):
                    input.setText(data[input.objectName()])
                elif isinstance(input, QDateTimeEdit):
                    input.setDateTime(data[input.objectName()])
                elif isinstance(input, QComboBox):
                    input.setCurrentIndex(input.findText(data[input.objectName()]))
            if elementId == 'e22':
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e23_cmbbx')
                input2.setCurrentIndex(input2.findText(data[input2.objectName()]))
            if elementId == 'e18':
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e19_cmbbx')
                input2.setCurrentIndex(input2.findText(data[input2.objectName()]))
            if elementId == 'e24':
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e25_lineEdit')
                input2.setText(data[input2.objectName()])
            if elementId == 'e9':
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e10_lineEdit')
                input2.setText(data[input2.objectName()])
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QDateTimeEdit, name='e10_dateTimeEdit')
                input2.setDateTime(data[input2.objectName()])
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e10_cmbbx')
                input2.setCurrentIndex(input2.findText(data[input2.objectName()]))

        def addItem():
            # print("ADD")
            if checkValidity():  # jeżeli pola są wypełnione
                newItem = QListWidgetItem()
                data = {}
                textList = []
                for input in inputs:
                    if isinstance(input, QLineEdit):
                        data[input.objectName()] = input.text()
                        textList.append(input.text())
                    if isinstance(input, QComboBox):
                        data[input.objectName()] = input.currentText()
                        textList.append(input.currentText())
                    if isinstance(input, QDateTimeEdit):
                        data[input.objectName()] = input.dateTime()
                        textList.append(input.dateTime().toString())

                if elementId == 'e22':
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e23_cmbbx')
                    data[input2.objectName()] = input2.currentText()
                    textList.append(input2.currentText())
                if elementId == 'e18':
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e19_cmbbx')
                    data[input2.objectName()] = input2.currentText()
                    textList.append(input2.currentText())
                if elementId == 'e24':
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e25_lineEdit')
                    data[input2.objectName()] = input2.text()
                    textList.append(input2.text())
                if elementId == 'e9':
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e10_lineEdit')
                    data[input2.objectName()] = input2.text()
                    textList.append(input2.text())
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QDateTimeEdit, name='e10_dateTimeEdit')
                    data[input2.objectName()] = input2.dateTime()
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e10_cmbbx')
                    data[input2.objectName()] = input2.currentText()
                    data['xlink'] = None

                newItem.setData(Qt.UserRole, QVariant(data))
                newItem.setText(" - ".join(textList))
                listWidget.addItem(newItem)
                clearDataFromListWidget()  # czyszczenie
            else:
                utils.showPopup("Wypełnij formularz mapy podkładowej",
                                'Musisz zdefiniować wartości dla wszystkich pól')
        def removeItem(listWidget):
            listWidget.takeItem(listWidget.currentRow())

        def setDefaultValues(elementId, listWidget):
            """ustawia domyślne wartości dla listWidget na podstawie słownika"""
            if elementId in dictionaries.metadataListWidgetsDefaultItemsDisabled.keys():
                dataList = dictionaries.metadataListWidgetsDefaultItemsDisabled[elementId]
                for data in dataList:
                    newItem = QListWidgetItem()
                    newItem.setData(Qt.UserRole, QVariant(data))
                    newItem.setText(list(data.values())[0])
                    newItem.setFlags(Qt.NoItemFlags)
                    listWidget.addItem(newItem)


        # print(listWidget.objectName())
        elementId = listWidget.objectName().split('_')[0]
        add_btn = utils.getWidgetByName(self, QPushButton, elementId + "_add_btn")
        remove_btn = utils.getWidgetByName(self, QPushButton, elementId + "_remove_btn")
        lineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_lineEdit")
        mailLineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_mail_lineEdit")
        nameLineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_name_lineEdit")
        dateTimeEdit = utils.getWidgetByName(self, QDateTimeEdit, elementId + "_dateTimeEdit")
        cmbbx = utils.getWidgetByName(self, QComboBox, elementId + "_cmbbx")
        setDefaultValues(elementId, listWidget)

        inputs = [lineEdit, dateTimeEdit, cmbbx, mailLineEdit, nameLineEdit]
        add_btn.clicked.connect(addItem)
        remove_btn.clicked.connect(lambda: removeItem(listWidget))
        listWidget.itemDoubleClicked.connect(getDataFromListWidget)

