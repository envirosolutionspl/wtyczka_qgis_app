# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit, QgsMapLayerComboBox
from qgis.PyQt.QtCore import Qt, QRegExp, QVariant
from qgis.PyQt.QtGui import QRegExpValidator, QPixmap
from . import dictionaries, utils


class NoScrollQComboBox(QComboBox):
    """Combobox bez scrolla"""

    def wheelEvent(self, event):
        event.ignore()


class NoScrollQgsDateTimeEdit(QgsDateTimeEdit):
    """QgsDateTimeEdit bez scrolla"""

    def wheelEvent(self, event):
        event.ignore()


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
                "rysunek",
                "zasiegPrzestrzenny"]

    def returnFormElements(self, formElements):
        for fe in formElements:
            print('\t'+fe.name)
            try:
                print(fe.refObject.objectName())
            except:
                print('W pominiętych')

    def removeForm(self, container):
        """usuwa zawartość kontenera(container), żeby zrobić miejsce na formularz"""
        container.takeWidget()

    def clearForm(self, container):
        """czyści pola formularza"""
        widgets = utils.getWidgets(
            layout=container,
            types=[QgsDateTimeEdit, QgsFilterLineEdit, QgsMapLayerComboBox, QComboBox])
        for widget in widgets[QgsDateTimeEdit]:
            widget.clear()
        for widget in widgets[QgsFilterLineEdit]:
            widget.clear()
        for widget in widgets[QgsMapLayerComboBox]:
            widget.setCurrentIndex(-1)
        for widget in widgets[QComboBox]:
            widget.setCurrentIndex(-1)

    def createForm(self, container, formElements):
        """tworzy formularz w miejscu kontenera (container), na podstawie listy obiektów klasy <FormElement>"""
        wgtMain = QWidget()
        vbox = QVBoxLayout(wgtMain)
        self.__loopFormElements(formElements, vbox)

        self.__preparePoziomHierarchii(vbox)
        container.setWidget(wgtMain)

    def __preparePoziomHierarchii(self, layout):
        """definiuje autouzupełnianie poziomHierarchii (INSPIRE)
        na podstawie typPlanu"""
        def typPlanu_cmbbx_currentTextChanged(currentText):
            poziomHierarchii_cmbbx.clear()
            wybor = dictionaries.typyPlanuPoziomyHierarchii[currentText]
            poziomHierarchii_cmbbx.addItems(wybor)

        # pobranie dynamicznie utworzonych obiektów UI
        poziomHierarchii_cmbbx = utils.layout_widget_by_name(
            layout, "poziomHierarchii_cmbbx")
        typPlanu_cmbbx = utils.layout_widget_by_name(layout, "typPlanu_cmbbx")
        if poziomHierarchii_cmbbx and typPlanu_cmbbx:   # jeżeli formularz zawiera te pola
            typPlanu_cmbbx.currentTextChanged.connect(
                typPlanu_cmbbx_currentTextChanged)

    def __loopFormElements(self, formElements, vbox, prefix=''):
        """Przerabia listę obiektów FormElements na GUI"""
        def createTable():
            referencja_lineEdit = utils.layout_widget_by_name(
                vbox2, name="referencja_lineEdit")
            aktualnosc_dateTimeEdit = utils.layout_widget_by_name(
                vbox2, name="aktualnosc_dateTimeEdit")
            lacze_lineEdit = utils.layout_widget_by_name(
                vbox2, name="lacze_lineEdit")
            lacze_lineEdit_nilReason_chkbx = utils.layout_widget_by_name(
                vbox2, name="lacze_lineEdit_nilReason_chkbx")
            lacze_lineEdit_nilReason_cmbbx = utils.layout_widget_by_name(
                vbox2, name="lacze_lineEdit_nilReason_cmbbx")
            lacze_lineEdit_nilReason_chkbx.stateChanged.connect(
                lambda: lacze_lineEdit.clear())

            def checkMapaPodkladowaValidity():
                if not referencja_lineEdit.text():
                    return False
                if not aktualnosc_dateTimeEdit.date():
                    return False
                if (
                        not lacze_lineEdit.text() and
                        not lacze_lineEdit_nilReason_chkbx.checkState()):
                    return False
                if (
                        not lacze_lineEdit.text() and
                        lacze_lineEdit_nilReason_chkbx.checkState() and
                        not lacze_lineEdit_nilReason_cmbbx.currentText()
                ):
                    return False
                return True

            def addItem():
                if checkMapaPodkladowaValidity():  # jeżeli ktoś wpisał referencję
                    newItem = QListWidgetItem()

                    newItem.setData(
                        Qt.UserRole,
                        QVariant({
                            "referencja_lineEdit": referencja_lineEdit.text(),
                            "aktualnosc_dateTimeEdit": aktualnosc_dateTimeEdit.dateTime(),
                            "lacze_lineEdit": lacze_lineEdit.text(),
                            "lacze_lineEdit_nilReason_chkbx": lacze_lineEdit_nilReason_chkbx.checkState(),
                            "lacze_lineEdit_nilReason_cmbbx": lacze_lineEdit_nilReason_cmbbx.currentIndex()
                        })
                    )
                    newItem.setText(referencja_lineEdit.text())
                    listWidget.addItem(newItem)
                    clearDataFromListWidget()   # czyszczenie
                else:
                    utils.showPopup("Wypełnij formularz mapy podkładowej",
                                    'Musisz zdefiniować wartości dla obowiązkowych pól:\n'
                                    '- referencja,\n'
                                    '- aktualnosc (aktualność),\n'
                                    '- lacze (łącze) - lub zaznaczyć "brak wartości" i wzkazać powód.')

            def removeItem():
                listWidget.takeItem(listWidget.currentRow())

            def clearDataFromListWidget():
                referencja_lineEdit.clear()
                aktualnosc_dateTimeEdit.clear()
                lacze_lineEdit.clear()
                lacze_lineEdit_nilReason_chkbx.setCheckState(False)
                lacze_lineEdit_nilReason_cmbbx.setCurrentIndex(0)

            def setDataToListWidget(listItem):
                data = listItem.data(Qt.UserRole)
                referencja_lineEdit.setText(data["referencja_lineEdit"])
                aktualnosc_dateTimeEdit.setDate(
                    data["aktualnosc_dateTimeEdit"])
                lacze_lineEdit.setText(data["lacze_lineEdit"])
                lacze_lineEdit_nilReason_chkbx.setCheckState(
                    data["lacze_lineEdit_nilReason_chkbx"])
                lacze_lineEdit_nilReason_cmbbx.setCurrentIndex(
                    data["lacze_lineEdit_nilReason_cmbbx"])

            # buttony
            btnHBox = QHBoxLayout()
            addBtn = QPushButton("Dodaj mapę podkładową")
            addBtn.clicked.connect(addItem)
            remBtn = QPushButton("Usuń mapę podkładową")
            remBtn.clicked.connect(removeItem)
            btnHBox.addWidget(addBtn)
            btnHBox.addWidget(remBtn)
            vbox2.addLayout(btnHBox)

            # QListWidget
            listWidget = QListWidget()
            listWidget.setObjectName("mapaPodkladowa_listWidget")
            listWidget.itemDoubleClicked.connect(setDataToListWidget)
            formElement.refObject = listWidget
            vbox2.addWidget(listWidget)

        for formElement in formElements:
            if (
                    formElement.type == 'gml:ReferenceType' or
                    formElement.type == "gml:AbstractFeatureMemberType" or
                    formElement.type == "gml:MultiSurfacePropertyType"
            ) and formElement.name in self.pomijane:
                continue  # pomiń element

            hbox = QHBoxLayout()  # wiersz formularza
            hbox.setObjectName(formElement.name + '_hbox')

            # label
            lbl = QLabel(text=prefix + formElement.name +
                         ('*' if formElement.minOccurs else ''))
            lbl.setObjectName(formElement.name + '_lbl')
            hbox.addWidget(lbl)

            input = self.__makeInput(formElement)
            formElement.refObject = input
            tooltipImg = self.__makeTooltip(formElement)

            if formElement.type == 'app:MapaPodkladowaPropertyType':
                groupbox = QGroupBox(formElement.name)
                groupbox.setObjectName("groupBox")
                vbox2 = QVBoxLayout()
                groupbox.setLayout(vbox2)
                vbox2.addLayout(hbox)

                hbox.addWidget(input)
                hbox.addWidget(tooltipImg)
                vbox.addWidget(groupbox)

                if formElement.isComplex():  # zawiera podrzędne elementy typu complex
                    # input.setEnabled(False)
                    input.setVisible(False)
                    # rekurencja dla obiektów wewntrznych
                    self.__loopFormElements(
                        formElement.innerFormElements, vbox2, '  - ')

                createTable()

            else:
                hbox.addWidget(input)

                if formElement.type == 'gmd:CI_Date_PropertyType':
                    input2 = NoScrollQComboBox()
                    input2.setObjectName(formElement.name + '_cmbbx')
                    input2.addItems(dictionaries.cI_DateTypeCode.keys())
                    formElement.refObject = input2

                    hbox.addWidget(input2)

                hbox.addWidget(tooltipImg)
                vbox.addLayout(hbox)
                if formElement.isComplex():  # zawiera podrzędne elementy typu complex
                    input.setEnabled(False)
                    # rekurencja dla obiektów wewntrznych
                    self.__loopFormElements(
                        formElement.innerFormElements, vbox, '  - ')

            if formElement.isNillable:  # dodaj dodatkowo checkbox i powód
                nilHbox = self.__makeNilHbox(input)
                vbox.addLayout(nilHbox)

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
        nilLbl2.setObjectName(
            nillableWidget.objectName() + 'nilReason' + '_lbl')
        nilLbl2.setEnabled(False)
        chckBox = QCheckBox(text='brak wartości')
        chckBox.setObjectName(
            nillableWidget.objectName() + '_nilReason' + '_chkbx')
        chckBox.stateChanged.connect(lambda: changeState())
        comboBox = QComboBox()
        comboBox.setObjectName(
            nillableWidget.objectName() + '_nilReason' + '_cmbbx')
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
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.ukladyOdniesieniaPrzestrzennego.keys())
        elif formElement.name == "typPlanu":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.typyPlanu.keys())
        elif formElement.name == "poziomHierarchii":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(
                reversed(list(dictionaries.poziomyHierarchii.keys())[1:]))
            # input.addItems(dictionaries.poziomyHierarchii.keys())
        elif formElement.name == "status":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.statusListaKodowa.keys())
        elif formElement.name == "dziennikUrzedowy":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.dziennikUrzedowyKod.keys())
        elif formElement.type == 'dateTime':
            input = NoScrollQgsDateTimeEdit()
            input.setObjectName(formElement.name + '_dateTimeEdit')
            input.clear()
        elif formElement.type == 'date':
            input = NoScrollQgsDateTimeEdit()
            input.setDisplayFormat('dd.MM.yyyy')
            input.setObjectName(formElement.name + '_dateTimeEdit')
            input.clear()
        elif formElement.type == 'gmd:CI_Date_PropertyType':
            input = NoScrollQgsDateTimeEdit()
            input.setDisplayFormat('dd.MM.yyyy')
            input.setObjectName(formElement.name + '_dateTimeEdit')
            input.clear()
        elif formElement.type == 'integer':
            input = QgsFilterLineEdit()
            # tylko liczby calkowite
            input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
            input.setObjectName(formElement.name + '_lineEdit')
        elif formElement.type == 'anyURI':
            input = QgsFilterLineEdit()
            # tylko ciąg znaków
            input.setValidator(QRegExpValidator(QRegExp(r"\S*")))
            input.setObjectName(formElement.name + '_lineEdit')
        else:
            input = QgsFilterLineEdit()
            input.setObjectName(formElement.name + '_lineEdit')

        # ustawienie podpowiedzi inputa (typ)
        input.setToolTip((formElement.type + ' - nillable')
                         if formElement.isNillable else formElement.type)

        # ustawienie domyślnych wartości
        fullFormElementName = formElement.form + ":" + formElement.name
        # print(fullFormElementName)
        if fullFormElementName in dictionaries.placeholders.keys():
            if isinstance(input, QLineEdit):  # dla pól tekstowych
                input.setText(
                    dictionaries.placeholders[fullFormElementName])
            elif isinstance(input, QComboBox):  # QComboBox
                pass

        # ustawienie podpowiedzi
        if fullFormElementName in dictionaries.placeholders.keys():
            input.setPlaceholderText(
                'np.: ' + dictionaries.placeholders[fullFormElementName])  # dla pól tekstowych

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
