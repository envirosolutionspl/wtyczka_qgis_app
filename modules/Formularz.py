# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit, QgsMapLayerComboBox
from qgis.PyQt.QtCore import Qt, QRegExp
from qgis.PyQt.QtGui import QRegExpValidator, QPixmap
from . import dictionaries



class Formularz:
    """Klasa reprezentująca formularz"""

    pomijane = ["aktNormatywnyPrzystapienie",
                "aktNormatywnyUchwalajacy",
                "aktNormatywnyZmieniajacy",
                "aktNormatywnyUchylajacy",
                "aktNormatywnyUniewazniajacy",
                "przystapienie",
                "uchwala",
                "zmienia",
                "uchyla",
                "uniewaznia",
                "plan",
                "dokument",
                "rysunek"]

    def removeForm(self, container):
        """usuwa zawartość kontenera(container), żeby zrobić miejsce na formularz"""
        container.takeWidget()

    def clearForm(self, container):
        """czyści pola formularza"""
        pass

    def createForm(self, container, formElements):
        """tworzy formularz w miejscu kontenera (container), na podstawie listy obiektów klasy <FormElement>"""
        wgtMain = QWidget()
        vbox = QVBoxLayout(wgtMain)
        self.__loopFormElements(formElements, vbox)

        container.setWidget(wgtMain)

    def __loopFormElements(self,formElements, vbox, prefix=''):
        """Przerabia listę obiektów FormElements na GUI"""

        for formElement in formElements:
            if (
                    formElement.type == 'gml:ReferenceType' or
                    formElement.type == "gml:AbstractFeatureMemberType"
            ) and formElement.name in self.pomijane:
                continue  # pomiń element

            hbox = QHBoxLayout()  # wiersz formularza
            hbox.setObjectName(formElement.name + '_hbox')

            # label
            lbl = QLabel(text=prefix + formElement.name + ('*' if formElement.minOccurs else ''))
            lbl.setObjectName(formElement.name + '_lbl')
            hbox.addWidget(lbl)

            input = self.__makeInput(formElement)
            tooltipImg = self.__makeTooltip(formElement)
            hbox.addWidget(input)
            hbox.addWidget(tooltipImg)
            vbox.addLayout(hbox)

            if formElement.isNillable:  # dodaj dodatkowo checkbox i powód
                nilHbox = self.__makeNilHbox(input)
                vbox.addLayout(nilHbox)

            if formElement.isComplex():  # zawiera podrzędne elementy typu complex
                input.setEnabled(False)
                self.__loopFormElements(formElement.innerFormElements, vbox, '  - ')    # rekurencja dla obiektów wewntrznych


    def __makeNilHbox(self, nillableWidget):
        """tworzy zestaw widgetów do obługi typu "nillable"""
        def changeState():
            currentState = chckBox.isChecked()
            if currentState:
                nilLbl2.setEnabled(True)
                nillableWidget.setEnabled(False)
                comboBox.setEnabled(True)
            else:
                nilLbl2.setEnabled(False)
                nillableWidget.setEnabled(True)
                comboBox.setEnabled(False)

        nilHbox = QHBoxLayout()
        nilLbl1 = QLabel(text='    ')
        nilLbl2 = QLabel(text='wskaż powód: ')
        nilLbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        nilLbl2.setObjectName(nillableWidget.objectName() + 'nilReason' + '_lbl')
        nilLbl2.setEnabled(False)
        chckBox = QCheckBox(text='brak wartości')
        chckBox.setObjectName(nillableWidget.objectName() + '_nilReason' + '_chkbx')
        chckBox.stateChanged.connect(lambda: changeState())
        comboBox = QComboBox()
        comboBox.setObjectName(nillableWidget.objectName() + '_nilReason' + '_cmbbx')
        comboBox.addItems(dictionaries.nilReasons.keys())
        comboBox.setEnabled(False)
        tooltipImg = QLabel()
        tooltipImg.setMaximumWidth(16)

        nilHbox.addWidget(nilLbl1)
        nilHbox.addWidget(chckBox)
        nilHbox.addWidget(nilLbl2)
        nilHbox.addWidget(comboBox)
        nilHbox.addWidget(tooltipImg)
        return nilHbox

    def __makeInput(self, formElement):
        # pole wprowadzania
        if formElement.name == "ukladOdniesieniaPrzestrzennego":
            input = QComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.ukladyOdniesieniaPrzestrzennego.keys())
        elif formElement.name == "typPlanu":
            input = QComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.typyPlanu.keys())
        elif formElement.name == "poziomHierarchii":
            input = QComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.poziomyHierarchii.keys())
        elif formElement.name == "status":
            input = QComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.statusListaKodowa.keys())
        elif formElement.name == "dziennikUrzedowy":
            input = QComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.dziennikUrzedowyKod.keys())
        elif formElement.type == 'dateTime':
            input = QgsDateTimeEdit()
            input.setObjectName(formElement.name + '_dateTimeEdit')
            input.clear()
        elif formElement.type == 'date' or formElement.type == 'gmd:CI_Date_PropertyType':
            input = QgsDateTimeEdit()
            input.setDisplayFormat('dd.MM.yyyy')
            input.setObjectName(formElement.name + '_dateEdit')
            input.clear()
        elif formElement.type == 'integer':
            input = QgsFilterLineEdit()
            input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))  # tylko liczby calkowite
            input.setObjectName(formElement.name + '_lineEdit')
        elif formElement.type == 'anyURI':
            input = QgsFilterLineEdit()
            input.setValidator(QRegExpValidator(QRegExp(r"\S*")))  # tylko liczby calkowite
            input.setObjectName(formElement.name + '_lineEdit')
        elif formElement.type == 'gml:MultiSurfacePropertyType':
            input = QgsFilterLineEdit()
            input.setEnabled(False)
            input.setText('< zasięg przestrzenny z warstwy >')
            input.setObjectName(formElement.name + '_lineEdit')
        else:
            input = QgsFilterLineEdit()
            input.setObjectName(formElement.name + '_lineEdit')

        # ustawienie podpowiedzi inputa (typ)
        input.setToolTip((formElement.type + ' - nillable') if formElement.isNillable else formElement.type)

        # ustawienie domyślnych wartości
        fullFormElementName = formElement.form + ":" + formElement.name
        if fullFormElementName in dictionaries.initialValues.keys():
            input.setText(dictionaries.initialValues[fullFormElementName])  # dla pól tekstowych

        # ustawienie podpowiedzi
        if fullFormElementName in dictionaries.placeholders.keys():
            input.setPlaceholderText('np.: ' + dictionaries.placeholders[fullFormElementName])  # dla pól tekstowych

        return input

    def __makeTooltip(self, formElement):
        tooltipImg = QLabel()
        p = QPixmap(':/plugins/wtyczka_app/img/info1.png')
        tooltipImg.setMaximumWidth(16)
        tooltipImg.setPixmap(p.scaled(16, 16, Qt.KeepAspectRatio))
        tooltipImg.setToolTip(
            "<FONT COLOR=black>%s</FONT>" % formElement.documentation)  # dodanie tooltip z documentation 'rich text' dla zawijania
        tooltipImg.setObjectName(formElement.name + '_tooltip')
        return tooltipImg
