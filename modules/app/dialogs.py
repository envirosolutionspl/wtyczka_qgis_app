# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu APP
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets



# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'pytanie_dialog_base.ui'))


class PytanieAppDialog(QtWidgets.QDialog, FORM_CLASS):
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


class ZbiorPrzygotowanieDialog(QtWidgets.QDialog, FORM_CLASS1):
    def __init__(self, parent=None):
        """Constructor."""
        super(ZbiorPrzygotowanieDialog, self).__init__(parent)
        self.setupUi(self)


FORM_CLASS2, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'raster_instrukcja_dialog_base.ui'))


class RasterInstrukcjaDialog(QtWidgets.QDialog, FORM_CLASS2):
    def __init__(self, parent=None):
        """Constructor."""
        super(RasterInstrukcjaDialog, self).__init__(parent)
        self.setupUi(self)

FORM_CLASS3, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'formularz_raster_dialog_base.ui'))


class RasterFormularzDialog(QtWidgets.QDialog, FORM_CLASS3):
    def __init__(self, parent=None):
        """Constructor."""
        super(RasterFormularzDialog, self).__init__(parent)
        self.setupUi(self)