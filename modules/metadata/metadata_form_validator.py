from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re
from .. import utils, dictionaries


def validateMetadataForm(dlg):
    """Walidacja poprawności formularza metadanych"""
    # Sprawdzanie czy wymagane pola są puste:
    for label in utils.getWidgetsByType(dlg, QLabel):
        if not re.match("e\d{1,2}_", label.objectName()):
            continue  # pomiń label, który nie jest częścią formularza

        elementId = label.objectName().split('_')[0]
        licznosc = dictionaries.licznoscMetadataFields[elementId]

        if licznosc == '1' and elementId != 'e25':   # wymagane 1
            if elementId == 'e13':
                dateTimeEdit = utils.getWidgetByName(dlg, QDateTimeEdit, elementId + "_dateTimeEdit")
                if not dateTimeEdit.dateTime():
                    return False, "Pole '%s' jest obowiązkowe. Musisz je wypełnić aby wygenerować plik metadanych" % label.text().strip('*')
            lineEdit = utils.getWidgetByName(dlg, QLineEdit, elementId + "_lineEdit")
            if lineEdit and not lineEdit.text().strip():
                return False, "Pole '%s' jest obowiązkowe. Musisz je wypełnić aby wygenerować plik metadanych" % label.text().strip('*')
        elif '+' in licznosc and licznosc[0] != 0:  # wielokrotnego wyboru wymagane
            listWidget = utils.getWidgetByName(dlg, QListWidget, elementId + "_listWidget")
            if listWidget.count() < int(licznosc[0]):
                return False, "Pole '%s' jest obowiązkowe. Musisz je wypełnić aby wygenerować plik metadanych. Minimalna ilość wystąpień to %s" % (label.text().strip('*'), licznosc[0])


    return [True]