from qgis.utils import iface
from . import (PytanieAppDialog, ZbiorPrzygotowanieDialog, RasterInstrukcjaDialog, RasterFormularzDialog,
               WektorFormularzDialog, DokumentyFormularzDialog, WektorInstrukcjaDialog, GenerowanieGMLDialog)
from .. import BaseModule, utils
from ..utils import showPopup
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.core import (
  QgsCoordinateReferenceSystem,
  QgsPointXY,
  QgsField,
  QgsFields,
  QgsFeature,
  QgsGeometry,
  QgsVectorLayer,
  QgsVectorFileWriter,
  QgsWkbTypes,
  QgsMapLayerProxyModel
)
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit
import os, os.path, time, datetime


class AppModule(BaseModule):
    metadaneDialog = None
    ustawieniaDialog = None
    pomocDialog = None

    def __init__(self, iface):
        self.iface = iface

        self.saved = False
        self.generated = False

    # region okna moduł app
        self.pytanieAppDialog = PytanieAppDialog()
        self.zbiorPrzygotowanieDialog = ZbiorPrzygotowanieDialog()
        self.rasterInstrukcjaDialog = RasterInstrukcjaDialog()
        self.rasterFormularzDialog = RasterFormularzDialog()
        self.wektorInstrukcjaDialog = WektorInstrukcjaDialog()
        self.wektorFormularzDialog = WektorFormularzDialog()
        self.dokumentyFormularzDialog = DokumentyFormularzDialog()
        self.generowanieGMLDialog = GenerowanieGMLDialog()
    # endregion

        self.pytanieAppDialog.zbior_btn.clicked.connect(self.pytanieAppDialog_zbior_btn_clicked)
        self.pytanieAppDialog.app_btn.clicked.connect(self.pytanieAppDialog_app_btn_clicked)
        self.pytanieAppDialog.settings_btn.clicked.connect(self.pytanieAppDialog_settings_btn_clicked)
        self.pytanieAppDialog.help_btn.clicked.connect(self.pytanieAppDialog_help_btn_clicked)

        self.rasterInstrukcjaDialog.next_btn.clicked.connect(self.rasterInstrukcjaDialog_next_btn_clicked)
        self.rasterInstrukcjaDialog.prev_btn.clicked.connect(self.rasterInstrukcjaDialog_prev_btn_clicked)

    # region rasterFormularzDialog

        self.rasterFormularzDialog.prev_btn.clicked.connect(self.rasterFormularzDialog_prev_btn_clicked)
        self.rasterFormularzDialog.next_btn.clicked.connect(self.checkSaveForms)
        self.rasterFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)

        # pobranie dynamicznie utworzonych obiektów UI
        self.idIIP_lineEdit = utils.getWidgetByName(
            layout=self.rasterFormularzDialog,
            seachObjectType=QgsFilterLineEdit,
            name="idIIP_lineEdit")
        self.lokalnyId_lineEdit = utils.getWidgetByName(
            layout=self.rasterFormularzDialog,
            seachObjectType=QgsFilterLineEdit,
            name="lokalnyId_lineEdit")
        self.przestrzenNazw_lineEdit = utils.getWidgetByName(
            layout=self.rasterFormularzDialog,
            seachObjectType=QgsFilterLineEdit,
            name="przestrzenNazw_lineEdit")
        self.wersjaId_lineEdit = utils.getWidgetByName(
            layout=self.rasterFormularzDialog,
            seachObjectType=QgsFilterLineEdit,
            name="wersjaId_lineEdit")

        # self.idIIP_lineEdit.setEnabled(False)
        # definicja Eventów dynamicznych obiektów UI
        self.lokalnyId_lineEdit.textChanged.connect(lambda: self.updateIdIPP())
        self.przestrzenNazw_lineEdit.textChanged.connect(lambda: self.updateIdIPP())
        self.wersjaId_lineEdit.textChanged.connect(lambda: self.updateIdIPP())

    # endregion

        self.wektorInstrukcjaDialog.next_btn.clicked.connect(self.wektorInstrukcjaDialog_next_btn_clicked)
        self.wektorInstrukcjaDialog.prev_btn.clicked.connect(self.wektorInstrukcjaDialog_prev_btn_clicked)
        self.wektorInstrukcjaDialog.generateTemporaryLayer_btn.clicked.connect(self.newEmptyLayer)
        self.wektorInstrukcjaDialog.chooseFile_btn.clicked.connect(self.openFile)
        self.wektorInstrukcjaDialog.layers_comboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

        self.wektorFormularzDialog.prev_btn.clicked.connect(self.wektorFormularzDialog_prev_btn_clicked)
        self.wektorFormularzDialog.next_btn.clicked.connect(self.checkSaveForms)
        self.wektorFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)

        self.dokumentyFormularzDialog.prev_btn.clicked.connect(self.dokumentyFormularzDialog_prev_btn_clicked)
        self.dokumentyFormularzDialog.next_btn.clicked.connect(self.checkSaveForms)
        self.dokumentyFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)

        self.generowanieGMLDialog.prev_btn.clicked.connect(self.generowanieGMLDialog_prev_btn_clicked)
        self.generowanieGMLDialog.generate_btn.clicked.connect(self.showPopupApp)
        self.generowanieGMLDialog.addElement_btn.clicked.connect(self.addTableContentGML)
        self.generowanieGMLDialog.deleteElement_btn.clicked.connect(self.deleteTableContentGML)
        header_gml = self.generowanieGMLDialog.filesTable_widget.horizontalHeader()
        header_gml.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header_gml.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header_gml.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.zbiorPrzygotowanieDialog.prev_btn.clicked.connect(self.zbiorPrzygotowanieDialog_prev_btn_clicked)
        self.zbiorPrzygotowanieDialog.next_btn.clicked.connect(self.checkSaveSet)
        self.zbiorPrzygotowanieDialog.validateAndGenerate_btn.clicked.connect(self.showPopupGenerate2)
        self.zbiorPrzygotowanieDialog.addElement_btn.clicked.connect(self.addTableContentSet)
        self.zbiorPrzygotowanieDialog.deleteElement_btn.clicked.connect(self.deleteTableContentSet)
        header_zbior = self.zbiorPrzygotowanieDialog.appTable_widget.horizontalHeader()  # auto resize kolumn
        header_zbior.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header_zbior.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.zbiorPrzygotowanieDialog.addFile_widget.setFilter("*.gml")

        # # pobranie widgetów danego typu
        # res = utils.getWidgetsByType(layout=self.rasterFormularzDialog, seachObjectType=QLabel)
        # print(res)


    """Event handlers"""

    # region pytanieAppDialog

    def pytanieAppDialog_app_btn_clicked(self):
        self.openNewDialog(self.rasterInstrukcjaDialog)
        self.listaOkienek.append(self.pytanieAppDialog)

    def pytanieAppDialog_zbior_btn_clicked(self):
        self.openNewDialog(self.zbiorPrzygotowanieDialog)
        self.listaOkienek.append(self.pytanieAppDialog)

    def pytanieAppDialog_settings_btn_clicked(self):
        self.ustawieniaDialog.exec()

    def pytanieAppDialog_help_btn_clicked(self):
        self.pomocDialog.exec()

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

    def updateIdIPP(self):
        self.idIIP_lineEdit.setText("%s - %s - %s" % (self.lokalnyId_lineEdit.text(), self.przestrzenNazw_lineEdit.text(), self.wersjaId_lineEdit.text()))
    # endregion

    # region wektorInstrukcjaDialog
    def wektorInstrukcjaDialog_next_btn_clicked(self):
        self.openNewDialog(self.wektorFormularzDialog)
        self.listaOkienek.append(self.wektorInstrukcjaDialog)

    def wektorInstrukcjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    # endregion

    # region wektorFormularzDialog
    def wektorFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def wektorFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.dokumentyFormularzDialog)
        self.listaOkienek.append(self.wektorFormularzDialog)

    # endregion

    # region dokumentyFormularzDialog
    def dokumentyFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def dokumentyFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.generowanieGMLDialog)
        self.listaOkienek.append(self.dokumentyFormularzDialog)

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

    # endregion

    """Helper methods"""
    # TODO dodać inne rozszerzenia plików wektorowych - najlepiej qgisowym narzędziem
    def openFile(self):
        shpFile = str(QFileDialog.getOpenFileName(filter=("Shapefiles (*.shp)"))[0])
        if shpFile:
            self.iface.addVectorLayer(shpFile, str.split(os.path.basename(shpFile), ".")[0], "ogr")

    def addTableContentGML(self):
        plik = str(QFileDialog.getOpenFileName(filter=("XML/GML files (*.xml *.gml)"))[0])
        param = True
        if plik:
            rows = self.generowanieGMLDialog.filesTable_widget.rowCount()
            if rows > 0:
                for i in range(rows):
                    item = self.generowanieGMLDialog.filesTable_widget.item(i, 0).text()
                    if plik == item:
                        param = False
                        self.showPopupSameRecord()
                        break
                if param:
                    self.tableContentGML(plik, rows)
            else:
                self.tableContentGML(plik, rows)

    def tableContentGML(self, file, rows):
        flags = Qt.ItemFlags(32)
        self.generowanieGMLDialog.filesTable_widget.setRowCount(rows + 1)
        self.generowanieGMLDialog.filesTable_widget.setItem(rows, 0, QTableWidgetItem(file))

        t = os.path.getmtime(file)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        item = QTableWidgetItem(mtime)
        item.setFlags(flags)
        self.generowanieGMLDialog.filesTable_widget.setItem(rows, 2, item)

    def deleteTableContentGML(self):
        row_num = self.generowanieGMLDialog.filesTable_widget.rowCount()
        if row_num > 0:
            do_usuniecia = self.generowanieGMLDialog.filesTable_widget.currentRow()
            self.generowanieGMLDialog.filesTable_widget.removeRow(do_usuniecia)
            self.generowanieGMLDialog.filesTable_widget.setCurrentCell(-1, -1)
        else:
            pass

    def addTableContentSet(self):
        plik = str(QFileDialog.getOpenFileName(filter=("GML file (*.gml)"))[0])
        param = True
        if plik:
            rows = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
            if rows > 0:
                for i in range(rows):
                    item = self.zbiorPrzygotowanieDialog.appTable_widget.item(i, 0).text()
                    if plik == item:
                        param = False
                        self.showPopupSameRecord()
                        break
                if param:
                    self.tableContentSet(plik, rows)
            else:
                self.tableContentSet(plik, rows)

    def tableContentSet(self, file, rows):
        flags = Qt.ItemFlags(32)
        self.zbiorPrzygotowanieDialog.appTable_widget.setRowCount(rows + 1)
        self.zbiorPrzygotowanieDialog.appTable_widget.setItem(rows, 0, QTableWidgetItem(file))

        t = os.path.getmtime(file)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        item = QTableWidgetItem(mtime)
        item.setFlags(flags)
        self.zbiorPrzygotowanieDialog.appTable_widget.setItem(rows, 1, item)

    def deleteTableContentSet(self):
        row_num = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
        if row_num > 0:
            do_usuniecia = self.zbiorPrzygotowanieDialog.appTable_widget.currentRow()
            self.zbiorPrzygotowanieDialog.appTable_widget.removeRow(do_usuniecia)
            self.zbiorPrzygotowanieDialog.appTable_widget.setCurrentCell(-1, -1)
        else:
            pass

    def newEmptyLayer(self):
        # TODO shp --> geopackage???,
        #  nadać poprawne atrybuty (czy są w ogóle potrzebne???),
        #  ograniczenie liczby obiektów do 1
        self.fn = QFileDialog.getSaveFileName(filter="Shapefile (*.shp)")[0]
        if self.fn:
            fields = QgsFields()
            fields.append(QgsField('idIIP', QVariant.String))
            fields.append(QgsField('nazwa', QVariant.String))
            writer = QgsVectorFileWriter(self.fn, 'UTF-8', fields, QgsWkbTypes.Polygon, QgsCoordinateReferenceSystem('EPSG:2180'), 'ESRI Shapefile')
            feat = QgsFeature()
            writer.addFeature(feat)
            iface.addVectorLayer(self.fn, '', 'ogr')

    """Popup windows"""

    def showPopupSaveForm(self):
        showPopup("Zapisz aktualny formularz", "Poprawnie zapisano formularz. W razie potrzeby wygenerowania kolejnego formularzu, należy zmodyfikować dane oraz zapisać formularz ponownie.")
        self.saved = True
        return self.saved

    def showPopupSameRecord(self):
        showPopup("Błąd tabeli", "Wybrany plik znajduje się już w tabeli")

    def showPopupGenerateLayer(self):
        showPopup("Wygeneruj warstwę", "Poprawnie utworzono pustą warstwę. Uzupełnij ją danymi wektorowymi oraz wypełnij atrybuty.")

    def showPopupGenerate(self):
        showPopup("Wygeneruj plik GML dla APP", "Poprawnie wygenerowano plik GML.")

    def showPopupGenerate2(self):
        showPopup("Wygeneruj plik GML dla zbioru APP", "Poprawnie wygenerowano plik GML.")
        self.generated = True
        return self.generated

    def showPopupApp(self):
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle('Czy chcesz utworzyć kolejny APP?')
        msg.setText('Wygenerowano plik GML dla APP. Czy chcesz stworzyć kolejny APP?')
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
        msg.setText('Czy chcesz przejść do tworzenia zbioru czy zakończyć pracę?')
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
                self.saved = False
            elif self.activeDlg == self.wektorFormularzDialog:
                self.openNewDialog(self.dokumentyFormularzDialog)
                self.listaOkienek.append(self.wektorFormularzDialog)
                self.saved = False
            elif self.activeDlg == self.dokumentyFormularzDialog:
                self.openNewDialog(self.generowanieGMLDialog)
                self.listaOkienek.append(self.dokumentyFormularzDialog)
                self.saved = False
        elif not self.saved:
            self.showPopupSaveForms()
        return self.saved

    def showPopupSaveForms(self):
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle('Niezapisany formularz')
        msg.setText('Formularz nie został zapisany. Czy na pewno chcesz przejść dalej?')
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
        elif not self.generated:
            self.showPopupSaveSet()
        return self.generated

    def showPopupSaveSet(self):
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle('Niewygenerowany GML dla zbioru')
        msg.setText('GML nie został jeszcze wygenerowany. Czy na pewno chcesz przejść do tworzenia metadanych?')
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