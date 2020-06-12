# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Metadata
 ***************************************************************************/
"""

import os

from PyQt5.QtWidgets import QMessageBox

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from .. import QDialogOverride



# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'walidacja_gmlxml_dialog_base.ui'))


class WalidacjaDialog(QDialogOverride, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(WalidacjaDialog, self).__init__(parent)
        self.setupUi(self)