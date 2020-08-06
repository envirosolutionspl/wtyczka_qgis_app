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

        # pola pojedyncze
        if licznosc == '1' and elementId != 'e25':   # wymagane 1
            if elementId == 'e13':
                dateTimeEdit = utils.getWidgetByName(dlg, QDateTimeEdit, elementId + "_dateTimeEdit")
                if not dateTimeEdit.dateTime():
                    return False, "Pole '%s' jest obowiązkowe. Musisz je wypełnić aby wygenerować plik metadanych" % label.text().strip('*')
            lineEdit = utils.getWidgetByName(dlg, QLineEdit, elementId + "_lineEdit")
            if lineEdit and not lineEdit.text().strip():
                return False, "Pole '%s' jest obowiązkowe. Musisz je wypełnić aby wygenerować plik metadanych" % label.text().strip('*')

        # pola wielokrotne wymagane
        elif '+' in licznosc and licznosc[0] != 0:  # wielokrotnego wyboru wymagane
            listWidget = utils.getWidgetByName(dlg, QListWidget, elementId + "_listWidget")
            if listWidget.count() < int(licznosc[0]):
                return False, "Pole '%s' jest obowiązkowe. Musisz je wypełnić aby wygenerować plik metadanych. Minimalna ilość wystąpień to %s" % (label.text().strip('*'), licznosc[0])

        # E9 pole słów kluczowych
        if elementId == 'e9':
            keywords = []
            for i in range(listWidget.count()):
                item = listWidget.item(i)
                data = item.data(Qt.UserRole)
                keywords.append(data['e9_lineEdit'])

            # Zagospodarowanie przestrzenne
            if 'Zagospodarowanie przestrzenne' not in keywords:
                return False, "W polu '%s' nie wprowadzono wszystkich wymaganych wartości.\nBrak klucza '%s'" % (
                label.text().strip('*'), 'Zagospodarowanie przestrzenne')
            # PlannedLandUse
            if 'PlannedLandUse' not in keywords:
                return False, "W polu '%s' nie wprowadzono wszystkich wymaganych wartości.\nBrak klucza '%s'" % (
                    label.text().strip('*'), 'PlannedLandUse')
            # zakres przestrzenny
            if not ('Regionalnym' in keywords or 'Lokalne' in keywords):
                return False, "W polu '%s' nie wprowadzono wszystkich wymaganych wartości.\nBrak klucza '%s', wymagane %s" % (
                    label.text().strip('*'), 'zakres przestrzenny', '\'Regionalnym\' lub \'Lokalne\'')
            # Poziom planu zagospodarowania przestrzennego
            if not ('regionalny' in keywords or 'lokalny' in keywords):
                return False, "W polu '%s' nie wprowadzono wszystkich wymaganych wartości.\nBrak klucza '%s', wymagane %s" % (
                    label.text().strip('*'), 'Poziom planu zagospodarowania przestrzennego', '\'regionalny\' lub \'lokalny\'')

        # E11 prostokąt ograniczający
        if elementId == 'e11':
            bboxes = []
            for i in range(listWidget.count()):
                item = listWidget.item(i)
                data = item.data(Qt.UserRole)
                bboxes.append(data['e11_lineEdit'])
            for bbox in bboxes:
                # zła ilość kropek lub przecinków
                if bbox.count(',') != 3 or bbox.count('.') > 4:
                    return False, "Niepoprawna wartość w polu '%s'.\nZły format prostokąta ograniczającego.\nPodano: '%s'\nPoprawny format to: '<xmin>,<xmax>,<ymin>,<ymax>'" % (
                        label.text().strip('*'), bbox)
                # sprawdzenie wartości
                bboxList = bbox.strip().split(',')
                xmin = float(bboxList[0])
                xmax = float(bboxList[1])
                ymin = float(bboxList[2])
                ymax = float(bboxList[3])
                if (
                        xmin > xmax or
                        ymin > ymax or
                        (xmin < -180 or xmin > 180) or
                        (xmax < -180 or xmax > 180) or
                        (ymin < -90 or ymin > 90) or
                        (ymax < -90 or ymax > 90)
                ):
                    return False, "Niepoprawna wartość w polu '%s'.\nZła wartość współrzędnych prostokąta ograniczającego.\nPodano: '%s'\nPoprawny format to: '<xmin>,<xmax>,<ymin>,<ymax>'\nx musi być w zakresie <-180;180>\ny musi być w zakresie <-90;90>" % (
                        label.text().strip('*'), bbox)

    return [True]