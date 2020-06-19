from PyQt5.QtWidgets import *
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit
from qgis.PyQt.QtCore import Qt, QRegExp
from qgis.PyQt.QtGui import QRegExpValidator

class Formularz:

    def clearForm(self, container):
        container.takeWidget()

    def createForm(self, container, formElements):

        wgtMain = QWidget()
        vbox = QVBoxLayout(wgtMain)
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
            elif formElement.type == 'date':
                input = QgsDateTimeEdit()
                input.setDisplayFormat('dd.MM.yyyy')
                input.setObjectName(formElement.name + '_dateEdit')
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
            btn = QPushButton(text='?')
            btn.setObjectName(formElement.name + 'Help_btn')
            btn.setMaximumWidth(50)
            btn.setToolTip("<FONT COLOR=black>%s</FONT>" % formElement.documentation)  # dodanie tooltip z documentation 'rich text' dla zawijania
            hbox.addWidget(btn)


            vbox.addLayout(hbox)
        container.setWidget(wgtMain)