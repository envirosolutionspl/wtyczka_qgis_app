# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit
from qgis.PyQt.QtCore import Qt, QRegExp
from qgis.PyQt.QtGui import QRegExpValidator, QPixmap

class Formularz:
    """Klasa reprezentująca formularz"""

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
        i = 0
        for formElement in formElements:
            hbox = QHBoxLayout()  # wiersz formularza

            # label
            lbl = QLabel(text=formElement.name + ('*' if formElement.minOccurs else ''))
            lbl.setObjectName(formElement.name + '_lbl')
            hbox.addWidget(lbl)

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
            hbox.addWidget(input)

            # PushButton "?"
            tooltipImg = QLabel()
            tooltipImg.setObjectName(formElement.name + '_tooltip')
            tooltipImg.setMaximumWidth(16)
            # tooltipImg.setScaledContents(True)
            tooltipImg.setToolTip("<FONT COLOR=black>%s</FONT>" % formElement.documentation)  # dodanie tooltip z documentation 'rich text' dla zawijania
            p = QPixmap(':/plugins/wtyczka_app/img/info1.png')
            tooltipImg.setPixmap(p.scaled(16, 16, Qt.KeepAspectRatio))
            hbox.addWidget(tooltipImg)
            vbox.addLayout(hbox)
        container.setWidget(wgtMain)

