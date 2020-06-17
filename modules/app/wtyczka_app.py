from . import (PytanieAppDialog, ZbiorPrzygotowanieDialog, RasterInstrukcjaDialog, RasterFormularzDialog,
               WektorFormularzDialog, DokumentyFormularzDialog, WektorInstrukcjaDialog, GenerowanieGMLDialog)
from .. import BaseModule
from ..utils import showPopup

from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
import os


class AppModule(BaseModule):
    metadaneDialog = None

    def __init__(self, iface):
        self.iface = iface

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

        # region eventy moduł app
        self.pytanieAppDialog.zbior_btn.clicked.connect(self.pytanieAppDialog_zbior_btn_clicked)
        self.pytanieAppDialog.app_btn.clicked.connect(self.pytanieAppDialog_app_btn_clicked)

        self.rasterInstrukcjaDialog.next_btn.clicked.connect(self.rasterInstrukcjaDialog_next_btn_clicked)
        self.rasterInstrukcjaDialog.prev_btn.clicked.connect(self.rasterInstrukcjaDialog_prev_btn_clicked)

        self.rasterFormularzDialog.prev_btn.clicked.connect(self.rasterFormularzDialog_prev_btn_clicked)
        self.rasterFormularzDialog.next_btn.clicked.connect(self.rasterFormularzDialog_next_btn_clicked)
        self.rasterFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)

        self.wektorInstrukcjaDialog.next_btn.clicked.connect(self.wektorInstrukcjaDialog_next_btn_clicked)
        self.wektorInstrukcjaDialog.prev_btn.clicked.connect(self.wektorInstrukcjaDialog_prev_btn_clicked)
        self.wektorInstrukcjaDialog.generateTemporaryLayer_btn.clicked.connect(self.showPopupGenerateLayer)
        self.wektorInstrukcjaDialog.chooseFile_btn.clicked.connect(self.openFile)


        self.wektorFormularzDialog.prev_btn.clicked.connect(self.wektorFormularzDialog_prev_btn_clicked)
        self.wektorFormularzDialog.next_btn.clicked.connect(self.wektorFormularzDialog_next_btn_clicked)
        self.wektorFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)

        self.dokumentyFormularzDialog.prev_btn.clicked.connect(self.dokumentyFormularzDialog_prev_btn_clicked)
        self.dokumentyFormularzDialog.next_btn.clicked.connect(self.dokumentyFormularzDialog_next_btn_clicked)
        self.dokumentyFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)

        self.generowanieGMLDialog.prev_btn.clicked.connect(self.generowanieGMLDialog_prev_btn_clicked)
        self.generowanieGMLDialog.next_btn.clicked.connect(self.generowanieGMLDialog_next_btn_clicked)
        self.generowanieGMLDialog.generate_btn.clicked.connect(self.showPopupGenerate)
        self.generowanieGMLDialog.yesMakeAnotherApp_radioBtn.toggled.connect(self.makeAnotherApp_radioBtn_toggled)
        self.generowanieGMLDialog.yesMakeSet_radioBtn.toggled.connect(self.makeSet_radioBtn_toggled)
        self.generowanieGMLDialog.addElement_btn.clicked.connect(self.addTableContentGML)
        self.generowanieGMLDialog.deleteElement_btn.clicked.connect(self.deleteTableContentGML)
        header_gml = self.generowanieGMLDialog.filesTable_widget.horizontalHeader()
        header_gml.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        self.zbiorPrzygotowanieDialog.prev_btn.clicked.connect(self.zbiorPrzygotowanieDialog_prev_btn_clicked)
        self.zbiorPrzygotowanieDialog.next_btn.clicked.connect(self.zbiorPrzygotowanieDialog_next_btn_clicked)
        self.zbiorPrzygotowanieDialog.validateAndGenerate_btn.clicked.connect(self.showPopupGenerate2)
        self.zbiorPrzygotowanieDialog.addElement_btn.clicked.connect(self.addTableContentSet)
        self.zbiorPrzygotowanieDialog.deleteElement_btn.clicked.connect(self.deleteTableContentSet)
        header_zbior = self.zbiorPrzygotowanieDialog.appTable_widget.horizontalHeader() #auto resize kolumn
        header_zbior.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.zbiorPrzygotowanieDialog.addFile_widget.setFilter("*.gml")
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
        if self.generowanieGMLDialog.yesMakeAnotherApp_radioBtn.isChecked():
            self.openNewDialog(self.rasterInstrukcjaDialog)
            self.listaOkienek.append(self.generowanieGMLDialog)
        if self.generowanieGMLDialog.noMakeAnotherApp_radioBtn.isChecked():
            if self.generowanieGMLDialog.yesMakeSet_radioBtn.isChecked():
                self.openNewDialog(self.zbiorPrzygotowanieDialog)
                self.listaOkienek.append(self.generowanieGMLDialog)
            if self.generowanieGMLDialog.noMakeSet_radioBtn.isChecked():
                self.generowanieGMLDialog.close()

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
    #setAdditionalItems nie działa, niepoprawny argument
    #dodać inne rozszerzenia
    def openFile(self):
        shpFile = str(QFileDialog.getOpenFileName(filter=("Shapefiles (*.shp)"))[0])
        #self.listaPlikow.append(shpFile)
        #self.wektorInstrukcjaDialog.layers_comboBox.setAdditionalItems(self.listaPlikow)
        if shpFile:
            self.iface.addVectorLayer(shpFile, str.split(os.path.basename(shpFile), ".")[0], "ogr")

    def addTableContentGML(self):
        plik = str(QFileDialog.getOpenFileName(filter=("XML/GML files (*.xml *.gml)"))[0])
        if plik:
            rows = self.generowanieGMLDialog.filesTable_widget.rowCount()
            self.generowanieGMLDialog.filesTable_widget.setRowCount(rows+1)
            self.generowanieGMLDialog.filesTable_widget.setItem(rows, 0, QTableWidgetItem(plik))

    def deleteTableContentGML(self):
        row_num = self.generowanieGMLDialog.filesTable_widget.rowCount()
        if row_num > 0:
            do_usuniecia = self.generowanieGMLDialog.filesTable_widget.currentRow()
            self.generowanieGMLDialog.filesTable_widget.removeRow(do_usuniecia)
        else:
            pass

    def addTableContentSet(self):
        plik = str(QFileDialog.getOpenFileName(filter=("GML file (*.gml)"))[0])
        if plik:
            rows = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
            self.zbiorPrzygotowanieDialog.appTable_widget.setRowCount(rows+1)
            self.zbiorPrzygotowanieDialog.appTable_widget.setItem(rows, 0, QTableWidgetItem(plik))

    def deleteTableContentSet(self):
        row_num = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
        if row_num > 0:
            do_usuniecia = self.zbiorPrzygotowanieDialog.appTable_widget.currentRow()
            self.zbiorPrzygotowanieDialog.appTable_widget.removeRow(do_usuniecia)
        else:
            pass

    """Popup windows"""
    def showPopupSaveForm(self):
        showPopup("Zapisz aktualny formularz", "Poprawnie zapisano formularz.")

    def showPopupGenerateLayer(self):
        showPopup("Wygeneruj warstwę", "Poprawnie utworzono pustą warstwę. Uzupełnij ją danymi wektorowymi oraz wypełnij atrybuty.")

    def showPopupGenerate(self):
        showPopup("Wygeneruj plik GML dla APP", "Poprawnie wygenerowano plik GML.")

    def showPopupGenerate2(self):
        showPopup("Wygeneruj plik GML dla zbioru APP", "Poprawnie wygenerowano plik GML.")