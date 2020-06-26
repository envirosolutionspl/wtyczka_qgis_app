from . import (UstawieniaDialog, PomocDialog)
from .. import BaseModule
from ..utils import showPopup

from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtCore import Qt
import os


class SettingsModule(BaseModule):

    def __init__(self, iface):
        self.iface = iface

        # region okno moduł settings
        self.ustawieniaDialog = UstawieniaDialog()
        # endregion

        # region eventy moduł settings

        # endregion

        # region okno moduł help
        self.pomocDialog = PomocDialog()
        # endregion

        # region eventy moduł help

        # endregion

    """Event handlers"""

    """Helper methods"""

    """Popup windows"""
