# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu APP
 ***************************************************************************/
"""

import os, sys

import PyQt5
from PyQt5.QtWidgets import QMessageBox, QPushButton

from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'pytanie_dialog_base.ui'))


class abc(QtWidgets.QDialog):
    def closeEvent(self, event):
        if self.sender() is None:
            reply = QMessageBox.question(self, 'Opuszczanie wtyczki APP',
                                         "Jesteś pewien, że chcesz opuścić wtyczkę?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


class PytanieAppDialog(abc, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(PytanieAppDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-views-with-auto-connect
        self.setupUi(self)
        # self.zbior_btn.clicked.connect(self.close)
        # self.app_btn.clicked.connect(self.close)



FORM_CLASS1, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'zbior_przygotowanie_dialog_base.ui'))


class ZbiorPrzygotowanieDialog(abc, FORM_CLASS1):
    def __init__(self, parent=None):
        """Constructor."""
        super(ZbiorPrzygotowanieDialog, self).__init__(parent)
        self.setupUi(self)



FORM_CLASS2, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'raster_instrukcja_dialog_base.ui'))


class RasterInstrukcjaDialog(abc, FORM_CLASS2):
    def __init__(self, parent=None):
        """Constructor."""
        super(RasterInstrukcjaDialog, self).__init__(parent)
        self.setupUi(self)


FORM_CLASS3, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'formularz_raster_dialog_base.ui'))


class RasterFormularzDialog(abc, FORM_CLASS3):
    def __init__(self, parent=None):
        """Constructor."""
        super(RasterFormularzDialog, self).__init__(parent)
        self.setupUi(self)



FORM_CLASS4, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'formularz_dokumenty_dialog_base.ui'))


class DokumentyFormularzDialog(abc, FORM_CLASS4):
    def __init__(self, parent=None):
        """Constructor."""
        super(DokumentyFormularzDialog, self).__init__(parent)
        self.setupUi(self)


FORM_CLASS5, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'formularz_wektor_dialog_base.ui'))


class WektorFormularzDialog(abc, FORM_CLASS5):
    def __init__(self, parent=None):
        """Constructor."""
        super(WektorFormularzDialog, self).__init__(parent)
        self.setupUi(self)


FORM_CLASS6, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'generowanie_gml_dialog_base.ui'))


class GenerowanieGMLDialog(abc, FORM_CLASS6):
    def __init__(self, parent=None):
        """Constructor."""
        super(GenerowanieGMLDialog, self).__init__(parent)
        self.setupUi(self)


FORM_CLASS7, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'wektor_instrukcja_dialog_base.ui'))


class WektorInstrukcjaDialog(abc, FORM_CLASS7):
    def __init__(self, parent=None):
        """Constructor."""
        super(WektorInstrukcjaDialog, self).__init__(parent)
        self.setupUi(self)