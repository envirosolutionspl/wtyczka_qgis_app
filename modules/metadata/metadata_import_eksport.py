from .. import dictionaries, utils
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRegExp, Qt
from collections import ChainMap
from xml.etree.ElementTree import Element,  Comment, tostring
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
"""

metadataElementDict - słownik zawierający elementID jako klucz np 'e23' i wartość elementu jako:
    - słownik - dla elementów wielokrotnych (tam gdzie jest QListWidget) - lista zawiera słowniki "data" przechowywane w QListWidgetItem.
      każdy słownik zawiera jako klucz - nazwę pola, jako wartość -wartość pola np. dla e9: [{'e9_lineEdit': 'Zagospodarowanie przestrzenne'}, {'e9_lineEdit': 'PlannedLandUse'}]
    - słownik - dla pojedynczych - zawierający nazwę pola i wartość np: e13: {'e13_cmbbx': 'utworzenie', 'e13_dateTimeEdit': PyQt5.QtCore.QDateTime(2020, 7, 26, 18, 16, 2, 978)}

"""
def formToMetadataElementDict(form):
    """pobiera wartości formularza do słownika metadataElementDict"""
    listWidgets = form.findChildren(QListWidget, QRegExp(r'.*'))
    lineEdits = form.findChildren(QLineEdit, QRegExp(r'.*'))
    dateTimeEdits = form.findChildren(QDateTimeEdit, QRegExp(r'.*'))
    comboBoxes = form.findChildren(QComboBox, QRegExp(r'.*'))
    singleWidgets = lineEdits + dateTimeEdits + comboBoxes
    metadataElementDict = {}
    for elementId, licznosc in dictionaries.licznoscMetadataFields.items():

        if not (licznosc == '01' or licznosc == '1'):   # pola wielokrotnego wyboru
            # pobierz listWidget
            listWidget = utils.getWidgetByName(layout=form, searchObjectType=QListWidget, name=elementId + '_listWidget')
            dataList = []
            for i in range(listWidget.count()):
                listWidgetItem = listWidget.item(i)
                data = listWidgetItem.data(Qt.UserRole) # slownik
                # if data is None:
                #     data = listWidgetItem.text()
                dataList.append(data)
            metadataElementDict[elementId] = dataList

        else:   # pola pojedynczego wyboru
            # pobierz wszystkie widgety o danym elementId
            tempList = []
            for input in [x for x in singleWidgets if x.objectName().startswith(elementId + '_')]:
                if isinstance(input, QLineEdit):
                    tempList.append({input.objectName(): input.text()})
                elif isinstance(input, QDateTimeEdit):
                    tempList.append({input.objectName(): input.dateTime()})
                elif isinstance(input, QComboBox):
                    tempList.append({input.objectName(): input.currentText()})

            metadataElementDict[elementId] = dict(ChainMap(*tempList))

    for k,v in metadataElementDict.items():
        print(k,dictionaries.licznoscMetadataFields[k],v)
    return metadataElementDict

def metadataElementDictToForm(metadataElementDict, targetForm):
    """aktualizuje formularz na podstawie słownika metadataElementDict"""
    pass

def metadataElementDictToXml(metadataElementDict):
    """tworzy XML na podstawie słownika metadataElementDict"""
    xml = None

    # Przestrzenie nazw ustawione na sztywno
    namespaces = {
        'xmlns:gco': "http://www.isotc211.org/2005/gco",
        'xmlns:gmx': "http://www.isotc211.org/2005/gmx",
        'xmlns:gmd': "http://www.isotc211.org/2005/gmd",
        'xmlns:gml': "http://www.opengis.net/gml",
        'xmlns:srv': "http://www.isotc211.org/2005/srv",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'xmlns:xs': "http://www.w3.org/2001/XMLSchema",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xsi:schemaLocation': "http://www.isotc211.org/2005/gmd http://schemas.opengis.net/iso/19139/20070417/gmd/gmd.xsd http://www.isotc211.org/2005/gmx http://schemas.opengis.net/iso/19139/20070417/gmx/gmx.xsd http://www.isotc211.org/2005/srv http://schemas.opengis.net/iso/19139/20070417/srv/1.0/srv.xsd"
    }

    """gmd:MD_Metadata"""
    root = ET.Element('gmd:MD_Metadata')
    for ns in namespaces.keys():
        root.set(ns, namespaces[ns])

    """gmd:fileIdentifier"""
    fileIdentifier = ET.SubElement(root, 'gmd:fileIdentifier')
    characterString = ET.SubElement(fileIdentifier, 'gco:CharacterString')
    characterString.text = metadataElementDict['e32']['e32_lineEdit']

    """gmd:language"""
    language = ET.SubElement(root, 'gmd:language')
    languageCode = ET.SubElement(language, 'gmd:LanguageCode', {'codeList': "http://www.loc.gov/standards/iso639-2/", 'codeListValue': "pol"})
    languageCode.text = metadataElementDict['e31']['e31_lineEdit']

    """gmd:characterSet"""
    for listItem in metadataElementDict['e7']:
        characterSet = ET.SubElement(root, 'gmd:characterSet')
        ET.SubElement(characterSet, 'gmd:MD_CharacterSetCode',
                                     {'codeList': "http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_CharacterSetCode", 'codeListValue': listItem['e7_cmbbx']})

    """gmd:hierarchyLevel"""
    hierarchyLevel = ET.SubElement(root, 'gmd:hierarchyLevel')
    ET.SubElement(hierarchyLevel, 'gmd:MD_ScopeCode',
                                 {'codeList': "http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_ScopeCode", 'codeListValue': metadataElementDict['e3']['e3_lineEdit']})



    xml = ET.ElementTree(root)

    print(minidom.parseString(tostring(root, encoding='utf-8', method='xml').decode('utf-8')).toprettyxml())
    # print(tostring(root, encoding='utf-8', method='xml').decode('utf-8'))
    return xml

def xmlToMetadataElementDict(xml):
    """słownik metadataElementDict na podstawie pliku XML"""
    metadataElementList = []
    return metadataElementList

