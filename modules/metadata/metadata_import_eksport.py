from .models import MetadataElement
from .. import dictionaries, utils
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRegExp, Qt

def formToMetadataElementList(form):
    """pobiera wartości formularza do listy MetadataElement"""
    metadataElementList = []
    listWidgets = form.findChildren(QListWidget, QRegExp(r'.*'))
    lineEdits = form.findChildren(QLineEdit, QRegExp(r'.*'))
    dateTimeEdits = form.findChildren(QDateTimeEdit, QRegExp(r'.*'))
    comboBoxes = form.findChildren(QComboBox, QRegExp(r'.*'))
    singleWidgets = lineEdits + dateTimeEdits + comboBoxes
    metadataElementDict = {}
    for elementId, licznosc in dictionaries.licznoscMetadataFields.items():
        # metadataElement = MetadataElement(elementId, licznosc)
        if not (licznosc == '01' or licznosc == '1'):
            # pobierz listWidget
            listWidget = utils.getWidgetByName(layout=form, searchObjectType=QListWidget, name=elementId + '_listWidget')
            dataList = []
            for i in range(listWidget.count()):
                listWidgetItem = listWidget.item(i)
                data = listWidgetItem.data(Qt.UserRole) # slownik
                if data is None:
                    data = listWidgetItem.text()
                dataList.append(data)
            metadataElementDict[elementId] = dataList
            print(licznosc, dataList)
            # metadataElement.setWidgets([x for x in listWidgets if x.objectName().startswith(elementId + '_')])
        else:
            # pobierz wszystkie widgety o danym elementId
            keys = [x.objectName() for x in singleWidgets if x.objectName().startswith(elementId + '_')]
            print(licznosc, keys)
            # metadataElementDict[elementId] =

            # metadataElement.setWidgets([x for x in singleWidgets if x.objectName().startswith(elementId + '_')])
        # metadataElementList.append(metadataElement)
    # for el in metadataElementList:
    #     print(el.elementId, el.licznosc, el.widgets)
    return metadataElementList

def metadataElementListToForm(metadataElementList):
    """aktualizuje formularz na podstawie listy MetadataElement"""
    pass

def metadataElementListToXml(metadataElementList):
    """tworzy XML na podstawie listy MetadataElement"""
    xml = None
    return xml

def xmlToMetadataElementList(xml):
    """listę MetadataElement na podstawie pliku XML"""
    metadataElementList = []
    return metadataElementList