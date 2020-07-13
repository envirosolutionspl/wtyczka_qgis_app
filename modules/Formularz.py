# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit, QgsMapLayerComboBox
from qgis.PyQt.QtCore import Qt, QRegExp
from qgis.PyQt.QtGui import QRegExpValidator, QPixmap
from . import utils


class Formularz:
    """Klasa reprezentująca formularz"""
    nilReasons = {
        "inapplicable": "nie dotyczy",
        "missing": "brakujący",
        "template": "szablon",
        "unknown": "nieznany",
        "withheld": "wstrzymany"}

    def removeForm(self, container):
        """usuwa zawartość kontenera(container), żeby zrobić miejsce na formularz"""
        container.takeWidget()

    def clearForm(self, container):
        """czyści pola formularza"""
        widgets = utils.getWidgets(
            layout=container,
            types=[QgsDateTimeEdit, QgsFilterLineEdit, QgsMapLayerComboBox])
        for widget in widgets[QgsDateTimeEdit]:
            widget.clear()
        for widget in widgets[QgsFilterLineEdit]:
            widget.clear()
        for widget in widgets[QgsMapLayerComboBox]:
            widget.clear()
        # widgets = utils.getWidgets(layout=container,  types=[
        #                            QLineEdit, QDateEdit])
        # for widget in widgets[QLineEdit]:
        #     widget.clear()

        # for w in widget[QLineEdit]:
        #     print(w)

    def createForm(self, container, formElements):
        """tworzy formularz w miejscu kontenera (container), na podstawie listy obiektów klasy <FormElement>"""
        wgtMain = QWidget()
        vbox = QVBoxLayout(wgtMain)
        pomijane = ["aktNormatywnyPrzystapienie",
                    "aktNormatywnyUchwalajacy",
                    "aktNormatywnyZmieniajacy",
                    "aktNormatywnyUchylajacy",
                    "aktNormatywnyUniewazniajacy",
                    "przystapienie",
                    "uchwala",
                    "zmienia",
                    "uchyla",
                    "uniewaznia"]
        for formElement in formElements:

            if formElement.type == 'gml:ReferenceType' and formElement.name in pomijane:
                continue    # pomiń element

            hbox = QHBoxLayout()  # wiersz formularza
            hbox.setObjectName(formElement.name + '_hbox')

            # label
            lbl = QLabel(text=formElement.name +
                         ('*' if formElement.minOccurs else ''))
            lbl.setObjectName(formElement.name + '_lbl')
            hbox.addWidget(lbl)

            input = self.__makeInput(formElement)
            tooltipImg = self.__makeTooltip(formElement)
            hbox.addWidget(input)
            hbox.addWidget(tooltipImg)
            vbox.addLayout(hbox)

            if formElement.isComplex():  # podrzędne elementy typu complex
                input.setEnabled(False)
                for formEl in formElement.innerFormElements:
                    subHbox = QHBoxLayout()  # podrzedny wiersz formularza
                    subHbox.setObjectName(formEl.name + '_hbox')
                    # label
                    subLbl = QLabel(text='       -   ' + formEl.name +
                                    ('*' if formElement.minOccurs else ''))
                    subLbl.setObjectName(formEl.name + '_lbl')
                    subHbox.addWidget(subLbl)

                    # input
                    subInput = self.__makeInput(formEl)

                    # tooltip
                    subTooltipImg = self.__makeTooltip(formEl)
                    subHbox.addWidget(subInput)
                    subHbox.addWidget(subTooltipImg)
                    vbox.addLayout(subHbox)

                    if formEl.isNillable:   # dodaj dodatkowo checkbox i powód
                        nilHbox = self.__makeNilHbox(subInput)
                        vbox.addLayout(nilHbox)

        container.setWidget(wgtMain)

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
        nilLbl2.setObjectName('nilReason' + '_lbl')
        nilLbl2.setEnabled(False)
        chckBox = QCheckBox(text='brak wartości')
        chckBox.setObjectName('nilReason' + '_chkbx')
        chckBox.stateChanged.connect(lambda: changeState())
        comboBox = QComboBox()
        comboBox.addItems(Formularz.nilReasons.keys())
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
        if formElement.type == 'dateTime':
            input = QgsDateTimeEdit()
            input.setObjectName(formElement.name + '_dateTimeEdit')
            input.clear()
        elif formElement.type == 'date':
            input = QgsDateTimeEdit()
            input.setDisplayFormat('dd.MM.yyyy')
            input.setObjectName(formElement.name + '_dateEdit')
            input.clear()
        elif formElement.type == 'integer':
            input = QgsFilterLineEdit()
            # tylko liczby calkowite
            input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
            input.setObjectName(formElement.name + '_lineEdit')
        elif formElement.type == 'anyURI':
            input = QgsFilterLineEdit()
            # tylko liczby calkowite
            input.setValidator(QRegExpValidator(QRegExp(r"\S*")))
            input.setObjectName(formElement.name + '_lineEdit')
        elif formElement.type == 'gml:ReferenceType' and formElement.name == 'plan':
            input = QgsMapLayerComboBox()
            input.setShowCrs(True)
            input.setFilters(QgsMapLayerProxyModel.RasterLayer)
            input.setObjectName(formElement.name + '_comboBox')
        elif formElement.type == 'gml:MultiSurfacePropertyType':
            input = QgsFilterLineEdit()
            input.setEnabled(False)
            input.setText('< zasięg przestrzenny z warstwy >')
            input.setObjectName(formElement.name + '_lineEdit')
        else:
            input = QgsFilterLineEdit()
            input.setObjectName(formElement.name + '_lineEdit')

        input.setToolTip((formElement.type + ' - nillable')
                         if formElement.isNillable else formElement.type)
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
