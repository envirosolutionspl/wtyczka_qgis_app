# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit
from qgis.PyQt.QtCore import Qt, QRegExp
from qgis.PyQt.QtGui import QRegExpValidator, QPixmap

class Formularz:
    """Klasa reprezentująca formularz"""
    tresc = 'abc'
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



        for formElement in formElements:
            hbox = QHBoxLayout()  # wiersz formularza
            subHboxList =[]
            # label
            lbl = QLabel(text=formElement.name + ('*' if formElement.minOccurs else ''))
            lbl.setObjectName(formElement.name + '_lbl')
            hbox.addWidget(lbl)

            input = self._makeInput(formElement)
            tooltipImg = self._makeTooltip(formElement)
            hbox.addWidget(input)
            hbox.addWidget(tooltipImg)
            vbox.addLayout(hbox)

            if formElement.isComplex:  # podrzędne elementy typu complex

                input.setEnabled(False)
                for formEl in formElement.innerFormElements:
                    subHbox = QHBoxLayout()  # podrzedny wiersz formularza
                    # label
                    subLbl = QLabel(text='       -   ' + formEl.name)
                    subLbl.setObjectName(formEl.name + '_lbl')
                    #input
                    subInput = self._makeInput(formEl)
                    # subInput.textChanged.connect(lambda: self._setXYZ(input,'ttt'))
                    #tooltip
                    tooltipImg = self._makeTooltip(formEl)

                    subHbox.addWidget(subLbl)
                    subHbox.addWidget(subInput)
                    subHbox.addWidget(tooltipImg)

                    subHboxList.append(subHbox)

                # dodanie wierszy obiektow complexType
                for subHbox in subHboxList:
                    vbox.addLayout(subHbox)
                subHboxList.clear()

        container.setWidget(wgtMain)
    def _setXYZ(self, object, text):
        # object.setText(text)
        print(object.displayText(), text)
        #object.setText(object.text() + text)

    def _makeInput(self, formElement):
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
            input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))  # tylko liczby calkowite
            input.setObjectName(formElement.name + '_lineEdit')
        elif formElement.type == 'anyURI':
            input = QgsFilterLineEdit()
            input.setValidator(QRegExpValidator(QRegExp(r"\S*")))  # tylko liczby calkowite
            input.setObjectName(formElement.name + '_lineEdit')
        else:
            input = QgsFilterLineEdit()
            input.setObjectName(formElement.name + '_lineEdit')
        input.setToolTip(formElement.type)
        return input

    def _makeTooltip(self, formElement):
        tooltipImg = QLabel()
        p = QPixmap(':/plugins/wtyczka_app/img/info1.png')
        tooltipImg.setMaximumWidth(16)
        tooltipImg.setPixmap(p.scaled(16, 16, Qt.KeepAspectRatio))
        tooltipImg.setToolTip(
            "<FONT COLOR=black>%s</FONT>" % formElement.documentation)  # dodanie tooltip z documentation 'rich text' dla zawijania
        tooltipImg.setObjectName(formElement.name + '_tooltip')
        return tooltipImg

