# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Metadata
 ***************************************************************************/
"""

import os

from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import Qt
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from .. import QDialogOverride, ButtonsDialog


title_metadata = 'Tworzenie / aktualizacja metadanych'
icon_metadata = ':/plugins/wtyczka_app/img/tworzenie.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'metadane_dialog_base.ui'))


class MetadaneDialog(QDialogOverride, FORM_CLASS, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(MetadaneDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title_metadata)
        self.setWindowIcon(QtGui.QIcon(icon_metadata))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        ButtonsDialog.__init__(self)