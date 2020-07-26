from qgis.utils import iface
from . import (PytanieAppDialog, ZbiorPrzygotowanieDialog, RasterInstrukcjaDialog, RasterFormularzDialog,
               WektorFormularzDialog, DokumentyFormularzDialog, WektorInstrukcjaDialog, GenerowanieGMLDialog)
from .. import BaseModule, utils, Formularz
from ..utils import showPopup
from ..models import AppTableModel
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.core import *
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit
import os
import os.path
import time
import datetime
import xml.etree.ElementTree as ET
import random
import ntpath
from lxml import etree


class AppModule(BaseModule):
    metadaneDialog = None
    # ustawieniaDialog = None
    # pomocDialog = None

    def __init__(self, iface):
        self.tableView = None
        self.iface = iface
        self.dataValidator = None  # inicjacja w głównym skrypcie wtyczki

        self.saved = False
        self.generated = False
        self.savedxml = False

    # region okna moduł app
        self.pytanieAppDialog = PytanieAppDialog()
        self.zbiorPrzygotowanieDialog = ZbiorPrzygotowanieDialog()
        self.rasterInstrukcjaDialog = RasterInstrukcjaDialog()
        self.rasterFormularzDialog = RasterFormularzDialog()
        self.wektorInstrukcjaDialog = WektorInstrukcjaDialog()
        self.wektorFormularzDialog = WektorFormularzDialog()
        self.dokumentyFormularzDialog = DokumentyFormularzDialog()
        self.generowanieGMLDialog = GenerowanieGMLDialog()

        # self.pytanieAppDialog.settings_btn.clicked.connect(self.__settings_btn_clicked)
    # endregion
    # region pytanieAppDialog
        self.pytanieAppDialog.zbior_btn.clicked.connect(
            self.pytanieAppDialog_zbior_btn_clicked)
        self.pytanieAppDialog.app_btn.clicked.connect(
            self.pytanieAppDialog_app_btn_clicked)
    # endregion
    # region rasterInstrukcjaDialog
        self.rasterInstrukcjaDialog.next_btn.clicked.connect(
            self.rasterInstrukcjaDialog_next_btn_clicked)
        self.rasterInstrukcjaDialog.prev_btn.clicked.connect(
            self.rasterInstrukcjaDialog_prev_btn_clicked)
    # endregion
    # region rasterFormularzDialog

        self.rasterFormularzDialog.prev_btn.clicked.connect(
            self.rasterFormularzDialog_prev_btn_clicked)
        self.rasterFormularzDialog.next_btn.clicked.connect(
            self.checkSaveForms)
        self.rasterFormularzDialog.saveForm_btn.clicked.connect(
            self.showPopupSaveForm)
        # zdarenia dynamicznie utworzonych obiektów UI związanych z IdIPP
        self.prepareIdIPP(formularz=self.rasterFormularzDialog)
        self.rasterFormularzDialog.clear_btn.clicked.connect(
            self.rasterFormularzDialog_clear_btn_clicked)

    # endregion
    # region wektorInstrukcjaDialog
        self.wektorInstrukcjaDialog.next_btn.clicked.connect(
            self.wektorInstrukcjaDialog_next_btn_clicked)
        self.wektorInstrukcjaDialog.prev_btn.clicked.connect(
            self.wektorInstrukcjaDialog_prev_btn_clicked)
        self.wektorInstrukcjaDialog.skip_btn.clicked.connect(
            self.wektorInstrukcjaDialog_skip_btn_clicked)
        self.wektorInstrukcjaDialog.generateTemporaryLayer_btn.clicked.connect(
            self.newEmptyLayer)
        self.wektorInstrukcjaDialog.layers_comboBox.setFilters(
            QgsMapLayerProxyModel.PolygonLayer)
        self.wektorInstrukcjaDialog.layers_comboBox.setShowCrs(True)
    # endregion
    # region wektorFormularzDialog
        self.wektorFormularzDialog.prev_btn.clicked.connect(
            self.wektorFormularzDialog_prev_btn_clicked)
        self.wektorFormularzDialog.next_btn.clicked.connect(
            self.checkSaveForms)
        self.wektorFormularzDialog.saveForm_btn.clicked.connect(
            self.showPopupSaveForm)
        self.wektorFormularzDialog.clear_btn.clicked.connect(
            self.wektorFormularzDialog_clear_btn_clicked)
        # zdarenia dynamicznie utworzonych obiektów UI związanych z IdIPP i mapapodkladowa
        self.prepareIdIPP(formularz=self.wektorFormularzDialog)
    # endregion
    # region dokumentyFormularzDialog
        self.dokumentyFormularzDialog.prev_btn.clicked.connect(
            self.dokumentyFormularzDialog_prev_btn_clicked)
        self.dokumentyFormularzDialog.next_btn.clicked.connect(
            self.checkSaveForms)
        self.dokumentyFormularzDialog.saveForm_btn.clicked.connect(
            self.showPopupSaveForm)
        self.dokumentyFormularzDialog.clear_btn.clicked.connect(
            self.dokumentyFormularzDialog_clear_btn_clicked)
        # zdarenia dynamicznie utworzonych obiektów UI związanych z IdIPP
        self.prepareIdIPP(formularz=self.dokumentyFormularzDialog)
    # endregion
    # region generowanieGMLDialog
        self.generowanieGMLDialog.prev_btn.clicked.connect(
            self.generowanieGMLDialog_prev_btn_clicked)
        self.generowanieGMLDialog.generate_btn.clicked.connect(
            self.generateAPP)
        self.generowanieGMLDialog.addElement_btn.clicked.connect(
            self.addTableContentGML)
        self.generowanieGMLDialog.deleteElement_btn.clicked.connect(
            self.deleteTableContentGML)

        # rozszerzanie kolumn
        header_gml = self.generowanieGMLDialog.filesTable_widget.horizontalHeader()
        for i in range(header_gml.count()):
            header_gml.setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeToContents)
    # endregion

    # region zbiorPrzygotowanieDialog
        self.zbiorPrzygotowanieDialog.prev_btn.clicked.connect(
            self.zbiorPrzygotowanieDialog_prev_btn_clicked)
        self.zbiorPrzygotowanieDialog.next_btn.clicked.connect(
            self.checkSaveSet)
        self.zbiorPrzygotowanieDialog.validateAndGenerate_btn.clicked.connect(
            self.validateAndGenerate_btn_clicked)
        self.zbiorPrzygotowanieDialog.addElement_btn.clicked.connect(
            self.addTableContentSet)
        self.zbiorPrzygotowanieDialog.deleteElement_btn.clicked.connect(
            self.deleteTableContentSet)

        # auto resize kolumn
        header_zbior = self.zbiorPrzygotowanieDialog.appTable_widget.horizontalHeader()
        for i in range(header_zbior.count()):
            header_zbior.setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeToContents)

        self.zbiorPrzygotowanieDialog.addFile_widget.setFilter(
            filter="pliki XML/GML (*.xml *.gml)")
    # endregion

    """Event handlers"""

    # region pytanieAppDialog

    def pytanieAppDialog_app_btn_clicked(self):
        self.openNewDialog(self.rasterInstrukcjaDialog)
        self.listaOkienek.append(self.pytanieAppDialog)

    def pytanieAppDialog_zbior_btn_clicked(self):
        self.openNewDialog(self.zbiorPrzygotowanieDialog)
        self.listaOkienek.append(self.pytanieAppDialog)

    # endregion

    # region rasterInstrukcjaDialog
    def rasterInstrukcjaDialog_next_btn_clicked(self):
        self.openNewDialog(self.rasterFormularzDialog)

        self.listaOkienek.append(self.rasterInstrukcjaDialog)

    def rasterInstrukcjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    # endregion

    # region rasterFormularzDialog
    def rasterFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def rasterFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.wektorInstrukcjaDialog)
        self.listaOkienek.append(self.rasterFormularzDialog)

    def rasterFormularzDialog_clear_btn_clicked(self):
        print(self.rasterFormularzDialog.form_scrollArea)
        self.rasterFormularzDialog.clearForm(
            self.rasterFormularzDialog.form_scrollArea)

    # endregion

    # region wektorInstrukcjaDialog

    def wektorInstrukcjaDialog_next_btn_clicked(self):
        def isGeomValid():
            """sprawdza czy geometria obrysu jest poprawna"""
            crs4326 = QgsCoordinateReferenceSystem(4326)  # WGS84
            layerCrs = self.obrysLayer.sourceCrs()  # z warstwy
            transform = QgsCoordinateTransform(
                layerCrs, crs4326, QgsProject.instance())

            layerExtent = self.obrysLayer.sourceExtent()
            layerExtent4326 = transform.transform(layerExtent)
            polandExtent4326 = QgsRectangle(
                14.0745211117, 49.0273953314, 24.0299857927, 54.8515359564)
            return polandExtent4326.intersects(layerExtent4326)

        self.obrysLayer = self.wektorInstrukcjaDialog.layers_comboBox.currentLayer()

        if not self.obrysLayer:   # brak wybranej warstwy
            showPopup("Błąd warstwy obrysu", "Nie wskazano warstwy z obrysem")
        elif self.obrysLayer.featureCount() > 1:     # niepoprawna ilość obiektów w warstwie

            self.showPopupAggregate(title="Błąd warstwy obrysu", text="Wybrana warstwa posiada obiekty w liczbie: %d.\nObrys może składać się wyłącznie z 1 jednego obiektu.\nCzy chcesz utworzyć zagregowaną warstwę o nazwie: granice_app_aggregated?" % (
                self.obrysLayer.featureCount()), layer=self.obrysLayer)
        elif self.obrysLayer.featureCount() == 0:
            showPopup("Błąd warstwy obrysu", "Wybrana warstwa posiada obiekty w liczbie: %d.\n" % (
                self.obrysLayer.featureCount()))
        elif not isGeomValid():     # niepoprawna geometria
            showPopup("Błąd warstwy obrysu",
                      "Niepoprawna geometria - obiekt musi leżeć w Polsce, sprawdź układ współrzędnych warstwy")
        else:   # wszystko OK z warstwą
            # zasiegPrzestrzenny = utils.getWidgetByName(
            #     layout=self.wektorFormularzDialog,
            #     searchObjectType=QgsFilterLineEdit,
            #     name="zasiegPrzestrzenny_lineEdit")
            # zasiegPrzestrzenny.setText(str(self.obrysLayer.sourceExtent()))
            # print(zasiegPrzestrzenny)
            self.openNewDialog(self.wektorFormularzDialog)
            self.listaOkienek.append(self.wektorInstrukcjaDialog)

    def wektorInstrukcjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def wektorInstrukcjaDialog_skip_btn_clicked(self):
        self.openNewDialog(self.dokumentyFormularzDialog)
        self.listaOkienek.append(self.wektorInstrukcjaDialog)

    # endregion

    # region wektorFormularzDialog
    def wektorFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def wektorFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.dokumentyFormularzDialog)
        self.listaOkienek.append(self.wektorFormularzDialog)

    def wektorFormularzDialog_clear_btn_clicked(self):
        self.wektorFormularzDialog.clearForm(
            self.wektorFormularzDialog.form_scrollArea)

    # endregion

    # region dokumentyFormularzDialog
    def dokumentyFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def dokumentyFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.generowanieGMLDialog)
        self.listaOkienek.append(self.dokumentyFormularzDialog)

    def dokumentyFormularzDialog_clear_btn_clicked(self):
        self.dokumentyFormularzDialog.clearForm(
            self.dokumentyFormularzDialog.form_scrollArea)

    # endregion

    # region generowanieGMLDialog
    def generowanieGMLDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def generowanieGMLDialog_next_btn_clicked(self):
        self.openNewDialog(self.zbiorPrzygotowanieDialog)
        self.listaOkienek.append(self.generowanieGMLDialog)
        # if self.generowanieGMLDialog.yesMakeAnotherApp_radioBtn.isChecked():
        #     self.openNewDialog(self.rasterInstrukcjaDialog)
        #     self.listaOkienek.append(self.generowanieGMLDialog)
        # if self.generowanieGMLDialog.noMakeAnotherApp_radioBtn.isChecked():
        #     if self.generowanieGMLDialog.yesMakeSet_radioBtn.isChecked():
        #         self.openNewDialog(self.zbiorPrzygotowanieDialog)
        #         self.listaOkienek.append(self.generowanieGMLDialog)
        #     if self.generowanieGMLDialog.noMakeSet_radioBtn.isChecked():
        #         self.generowanieGMLDialog.close()

    def makeAnotherApp_radioBtn_toggled(self, setYes):
        if setYes:  # tak - utworzenie kolejnego APP
            self.generowanieGMLDialog.next_btn.setText("Dalej")
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setChecked(False)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setChecked(False)
            self.generowanieGMLDialog.questionMakeSet_lbl.setEnabled(False)
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setEnabled(False)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setEnabled(False)
        else:  # nie
            self.generowanieGMLDialog.questionMakeSet_lbl.setEnabled(True)
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setEnabled(True)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setEnabled(True)
            if self.generowanieGMLDialog.noMakeSet_radioBtn.isChecked():
                self.generowanieGMLDialog.next_btn.setText("Zakończ")

    def makeSet_radioBtn_toggled(self, setYes):
        if setYes:  # finalne tworzenie zbioru app
            self.generowanieGMLDialog.next_btn.setText("Dalej")
        else:  # zakończ działanie wtyczki
            self.generowanieGMLDialog.next_btn.setText("Zakończ")

    # endregion

    # region zbiorPrzygotowanieDialog
    def zbiorPrzygotowanieDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def zbiorPrzygotowanieDialog_next_btn_clicked(self):
        self.openNewDialog(self.metadaneDialog)
        self.listaOkienek.append(self.zbiorPrzygotowanieDialog)
        self.metadaneDialog.prev_btn.setEnabled(True)

    def validateAndGenerate_btn_clicked(self):

        files = []
        gmlPaths = []
        appTable_widget = utils.getWidgetByName(
            layout=self.zbiorPrzygotowanieDialog,
            searchObjectType=QTableWidget,
            name="appTable_widget")
        for rowId in range(appTable_widget.rowCount()):
            xmlPath = os.path.join(appTable_widget.item(rowId, 0).text())
            xmlDate = appTable_widget.item(rowId, 1).text()
            files.append(AppTableModel(rowId, xmlPath, xmlDate))
            gmlPaths.append(xmlPath)
        # files = [os.path.join(os.path.dirname(__file__), "../validator", 'appExample_pzpw_v001.xml')] # test

        # Sprawdzenie poprawności każdego z plików składowych
        for file in files:
            # nie zwalidowano poprawnie
            if not self.validateFile(path=file.path, validator=self.dataValidator):
                return False

        # Sprawdzenie zależności geometrycznych miedzy GMLami
        result = utils.checkZbiorGeometryValidity(gmlPaths)
        if not result[0]:  # niepoprawne zależności geometryczne
            trescBledu = result[1]
            self.iface.messageBar().pushCritical("Błąd geometrii zbioru:", trescBledu)
            return False

        # TODO: Łączenie APP w zbiór

        self.iface.messageBar().pushSuccess("Generowanie zbioru:",
                                            "Pomyślnie wygenerowano zbiór APP.")
        showPopup("Wygeneruj plik GML dla zbioru APP",
                  "Poprawnie wygenerowano plik GML.")
        self.generated = True
        return True

    # endregion

    """Helper methods"""

    def addTableContentGML(self):
        plik = str(QFileDialog.getOpenFileName(
            filter="pliki XML/GML (*.xml *.gml)")[0])
        param = True
        if plik:
            rows = self.generowanieGMLDialog.filesTable_widget.rowCount()
            if rows > 0:
                for i in range(rows):
                    item = self.generowanieGMLDialog.filesTable_widget.item(
                        i, 0).toolTip()
                    if plik == item:
                        param = False
                        showPopup("Błąd tabeli",
                                  "Wybrany plik znajduje się już w tabeli")
                        break
                if param:
                    self.tableContentGML(plik, rows)
            else:
                self.tableContentGML(plik, rows)

    def tableContentGML(self, file, rows):
        # data modyfikacji
        def path_leaf(file):
            head, tail = ntpath.split(file)
            return tail or ntpath.basename(head)
        file2 = path_leaf(file)
        flags = Qt.ItemFlags(32)
        self.generowanieGMLDialog.filesTable_widget.setRowCount(rows + 1)
        self.generowanieGMLDialog.filesTable_widget.setItem(
            rows, 0, QTableWidgetItem(file2))
        test = self.generowanieGMLDialog.filesTable_widget.item(rows, 0)
        test.setToolTip(file)

        t = os.path.getmtime(file)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        item = QTableWidgetItem(mtime)
        item.setFlags(flags)
        self.generowanieGMLDialog.filesTable_widget.setItem(rows, 2, item)

        # Ustawianie rodzaju dokumentu
        docNames = {
            'AktPlanowaniaPrzestrzennego': 'APP',
            'RysunekAktuPlanowniaPrzestrzenego': 'Rysunek APP',
            'DokumentFormalny': 'Dokument Formalny'
        }
        try:
            docName = docNames[utils.getDocType(file)]
        except:
            docName = ''
        if docName == '':
            utils.showPopup(title='Błędny plik',
                            text='Wczytano błędny plik: %s' % file2)
        rodzaj = ['Dokument Formalny', 'APP', 'Rysunek APP']
        item2 = QTableWidgetItem(docName)
        item2.setFlags(flags)
        self.generowanieGMLDialog.filesTable_widget.setItem(rows, 1, item2)

        # relacja z APP
        if self.generowanieGMLDialog.filesTable_widget.item(rows, 1).text() == 'Dokument Formalny':
            c = QComboBox()
            c.addItems(['przystąpienie', 'uchwala', 'zmienia',
                        'uchyla', 'unieważnia', 'inna'])
            i = self.generowanieGMLDialog.filesTable_widget.model().index(rows, 3)
            self.generowanieGMLDialog.filesTable_widget.setCellWidget(
                rows, 3, c)
            print(self.generowanieGMLDialog.filesTable_widget.cellWidget(
                rows, 3).currentText())
        else:
            empty = QTableWidgetItem('')
            empty.setFlags(flags)
            self.generowanieGMLDialog.filesTable_widget.setItem(rows, 3, empty)

    def deleteTableContentGML(self):
        row_num = self.generowanieGMLDialog.filesTable_widget.rowCount()
        if row_num > 0:
            do_usuniecia = self.generowanieGMLDialog.filesTable_widget.currentRow()
            self.generowanieGMLDialog.filesTable_widget.removeRow(do_usuniecia)
            self.generowanieGMLDialog.filesTable_widget.setCurrentCell(-1, -1)
        else:
            pass

    def getTableContent(self):
        content = []
        row_num = self.generowanieGMLDialog.filesTable_widget.rowCount()
        for i in range(row_num):
            item = self.generowanieGMLDialog.filesTable_widget.item(
                i, 0).toolTip()
            try:
                relation = self.generowanieGMLDialog.filesTable_widget.cellWidget(
                    i, 3).currentText()
            except:
                relation = ''
            content.append([item, relation])
        return content  # ścieżki do plików

    def generateAPP(self):  # Generowanie pliku z APP
        self.fn = QFileDialog.getSaveFileName(
            filter="XML Files (*.xml)")[0]
        if self.fn:
            docList = self.getTableContent()

            xml_string = utils.mergeDocsToAPP(docList)
            if xml_string != '':
                myfile = open(self.fn, "w", encoding='utf-8')
                myfile.write(xml_string)
                self.showPopupApp()
# Zbiór

    def addTableContentSet(self):
        plik = str(QFileDialog.getOpenFileName(
            filter="pliki XML/GML (*.xml *.gml)")[0])
        param = True
        if plik:
            rows = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
            if rows > 0:
                for i in range(rows):
                    item = self.zbiorPrzygotowanieDialog.appTable_widget.item(
                        i, 0).text()
                    if plik == item:
                        param = False
                        showPopup("Błąd tabeli",
                                  "Wybrany plik znajduje się już w tabeli")
                        break
                if param:
                    self.tableContentSet(plik, rows)
            else:
                self.tableContentSet(plik, rows)

    def tableContentSet(self, file, rows):
        flags = Qt.ItemFlags(32)
        self.zbiorPrzygotowanieDialog.appTable_widget.setRowCount(rows + 1)
        self.zbiorPrzygotowanieDialog.appTable_widget.setItem(
            rows, 0, QTableWidgetItem(file))

        t = os.path.getmtime(file)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        item = QTableWidgetItem(mtime)
        item.setFlags(flags)
        self.zbiorPrzygotowanieDialog.appTable_widget.setItem(rows, 1, item)

    def deleteTableContentSet(self):
        row_num = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
        if row_num > 0:
            do_usuniecia = self.zbiorPrzygotowanieDialog.appTable_widget.currentRow()
            self.zbiorPrzygotowanieDialog.appTable_widget.removeRow(
                do_usuniecia)
            self.zbiorPrzygotowanieDialog.appTable_widget.setCurrentCell(
                -1, -1)
        else:
            pass

    def fieldsDefinition(self, fields):
        fieldDef = ''
        for field in fields:
            form = Formularz()
            # TODO Czy mamy uniemożliwiać wpisywanie wartości dla ReferenceType
            if field.name not in form.pomijane and field.type != 'gml:ReferenceType':
                if field.isComplex():  # zawiera podrzędne elementy typu complex
                    for fieldElements in field.innerFormElements:
                        fieldDef += '&field=%s:%s' % (
                            fieldElements.name, fieldElements.type)
                    continue
                fieldDef += '&field=%s:%s' % (field.name, field.type)
        return(fieldDef)

    def newEmptyLayer(self):
        fields = utils.createFormElements(
            'AktPlanowaniaPrzestrzennegoType')
        layer = QgsVectorLayer(
            'multipolygon?crs=epsg:2180' +
            self.fieldsDefinition(fields=fields), 'granice_app', 'memory')
        QgsProject.instance().addMapLayer(layer)

        self.iface.messageBar().pushSuccess("Utworzenie warstwy:",
                                            "Stworzono warstwę typu multipoligon do wektoryzacji.")
        showPopup("Wygeneruj warstwę",
                  "Poprawnie utworzono pustą warstwę. Uzupełnij ją danymi przestrzennymi.")

    """Popup windows"""

    def showPopupSaveForm(self):
        if utils.isFormFilled(self.activeDlg):
            self.fn = QFileDialog.getSaveFileName(
                filter="XML Files (*.xml)")[0]
            if self.fn:
                self.saved = True
                # TODO wypełnienie xml wartościami z xml
                try:
                    self.obrysLayer = self.wektorInstrukcjaDialog.layers_comboBox.currentLayer()
                except:
                    self.obrysLayer = None
                data = utils.createXmlData(self.activeDlg, self.obrysLayer)

                mydata = ET.tostring(data)
                root = etree.XML(mydata)

                xml_string = etree.tostring(root, xml_declaration=True,
                                            encoding='utf-8', pretty_print=True).decode('utf-8')
                myfile = open(self.fn, "w", encoding='utf-8')
                myfile.write(xml_string)

                showPopup("Zapisz aktualny formularz",
                          "Poprawnie zapisano formularz. W razie potrzeby wygenerowania kolejnego formularza, należy zmodyfikować dane oraz zapisać formularz ponownie.")
        return self.saved

    def showPopupAggregate(self, title, text, layer):
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(text)
        yes = msg.addButton(
            'Tak', QtWidgets.QMessageBox.AcceptRole)
        no = msg.addButton(
            'Nie', QtWidgets.QMessageBox.RejectRole)
        msg.setDefaultButton(yes)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is yes:
            self.aggregateLayer(layer)

    def aggregateLayer(self, layer):
        # Aggregate
        alg_params = {
            'AGGREGATES': [],
            'GROUP_BY': 'NULL',
            'INPUT': layer,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        import processing
        aggregated = processing.run('native:aggregate', alg_params)
        aggregated['OUTPUT'].setName('granice_app_aggregated')
        QgsProject.instance().addMapLayer(aggregated['OUTPUT'])

    def showPopupApp(self):
        # Popup generowanie APP
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle('Czy chcesz utworzyć kolejny APP?')
        msg.setText(
            'Wygenerowano plik GML dla APP. Czy chcesz stworzyć kolejny APP?')
        yes = msg.addButton(
            'Tak', QtWidgets.QMessageBox.AcceptRole)
        no = msg.addButton(
            'Nie', QtWidgets.QMessageBox.AcceptRole)
        cancel = msg.addButton(
            'Anuluj', QtWidgets.QMessageBox.RejectRole)
        msg.setDefaultButton(yes)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is yes:
            self.openNewDialog(self.rasterInstrukcjaDialog)
            self.listaOkienek.append(self.generowanieGMLDialog)
        elif msg.clickedButton() is no:
            self.showPopupSet()

    def showPopupSet(self):
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle('Czy chcesz utworzyć zbiór APP?')
        msg.setText(
            'Czy chcesz przejść do tworzenia zbioru czy zakończyć pracę?')
        set = msg.addButton(
            'Tworzenie zbioru', QtWidgets.QMessageBox.AcceptRole)
        cancel = msg.addButton(
            'Anuluj', QtWidgets.QMessageBox.RejectRole)
        quit = msg.addButton(
            'Zakończ', QtWidgets.QMessageBox.AcceptRole)

        msg.setDefaultButton(set)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is set:
            self.openNewDialog(self.zbiorPrzygotowanieDialog)
            self.listaOkienek.append(self.generowanieGMLDialog)
        elif msg.clickedButton() is quit:
            self.generowanieGMLDialog.close()

    def checkSaveForms(self):
        if self.saved:
            if self.activeDlg == self.rasterFormularzDialog:
                self.openNewDialog(self.wektorInstrukcjaDialog)
                self.listaOkienek.append(self.rasterFormularzDialog)
            elif self.activeDlg == self.wektorFormularzDialog:
                self.openNewDialog(self.dokumentyFormularzDialog)
                self.listaOkienek.append(self.wektorFormularzDialog)
            elif self.activeDlg == self.dokumentyFormularzDialog:
                self.openNewDialog(self.generowanieGMLDialog)
                self.listaOkienek.append(self.dokumentyFormularzDialog)
            self.saved = False
        else:
            self.showPopupSaveForms()
        return self.saved

    def showPopupSaveForms(self):
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle('Niezapisany formularz')
        msg.setText(
            'Formularz nie został zapisany. Czy na pewno chcesz przejść dalej?')
        yes = msg.addButton(
            'Tak', QtWidgets.QMessageBox.AcceptRole)
        no = msg.addButton(
            'Nie', QtWidgets.QMessageBox.RejectRole)
        msg.setDefaultButton(no)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is yes:
            if self.activeDlg == self.rasterFormularzDialog:
                self.openNewDialog(self.wektorInstrukcjaDialog)
                self.listaOkienek.append(self.rasterFormularzDialog)
            elif self.activeDlg == self.wektorFormularzDialog:
                self.openNewDialog(self.dokumentyFormularzDialog)
                self.listaOkienek.append(self.wektorFormularzDialog)
            elif self.activeDlg == self.dokumentyFormularzDialog:
                self.openNewDialog(self.generowanieGMLDialog)
                self.listaOkienek.append(self.dokumentyFormularzDialog)

    def checkSaveSet(self):
        if self.generated:
            self.openNewDialog(self.metadaneDialog)
            self.listaOkienek.append(self.zbiorPrzygotowanieDialog)
            self.generated = False
        else:
            self.showPopupSaveSet()
        return False

    def showPopupSaveSet(self):
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle('Niewygenerowany GML dla zbioru')
        msg.setText(
            'GML nie został jeszcze wygenerowany. Czy na pewno chcesz przejść do tworzenia metadanych?')
        yes = msg.addButton(
            'Tak', QtWidgets.QMessageBox.AcceptRole)
        no = msg.addButton(
            'Nie', QtWidgets.QMessageBox.RejectRole)
        msg.setDefaultButton(no)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is yes:
            self.openNewDialog(self.metadaneDialog)
            self.listaOkienek.append(self.zbiorPrzygotowanieDialog)

    def prepareIdIPP(self, formularz):
        """definuje autouzupełnianie idIPP na podstawie zagnieżdzonych pól"""
        def updateIdIPP():
            idIIP_lineEdit.setText("%s_%s_%s" % (
                przestrzenNazw_lineEdit.text().replace("/", "_"),
                lokalnyId_lineEdit.text(), wersjaId_lineEdit.text()))

        # pobranie dynamicznie utworzonych obiektów UI
        idIIP_lineEdit = utils.getWidgetByName(
            layout=formularz,
            searchObjectType=QgsFilterLineEdit,
            name="idIIP_lineEdit")
        lokalnyId_lineEdit = utils.getWidgetByName(
            layout=formularz,
            searchObjectType=QgsFilterLineEdit,
            name="lokalnyId_lineEdit")
        przestrzenNazw_lineEdit = utils.getWidgetByName(
            layout=formularz,
            searchObjectType=QgsFilterLineEdit,
            name="przestrzenNazw_lineEdit")
        wersjaId_lineEdit = utils.getWidgetByName(
            layout=formularz,
            searchObjectType=QgsFilterLineEdit,
            name="wersjaId_lineEdit")

        # definicja Eventów dynamicznych obiektów UI
        lokalnyId_lineEdit.textChanged.connect(lambda: updateIdIPP())
        przestrzenNazw_lineEdit.textChanged.connect(lambda: updateIdIPP())
        wersjaId_lineEdit.textChanged.connect(lambda: updateIdIPP())
