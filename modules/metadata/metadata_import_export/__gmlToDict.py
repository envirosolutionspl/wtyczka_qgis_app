from .. import dictionaries, utils
import xml.etree.ElementTree as ET
import re
from PyQt5.QtCore import QDateTime
from qgis.core import QgsVectorLayer

def appGmlToMetadataElementDict(gmlPath):
    """słownik metadataElementDict na podstawie pliku zbioru APP"""
    metadataElementDict = {}

    ns = {'gco': "http://www.isotc211.org/2005/gco",
          'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gml': "http://www.opengis.net/gml/3.2",
          'wfs': "http://www.opengis.net/wfs/2.0",
          'xlink': "http://www.w3.org/1999/xlink",
          'xsi': "http://www.w3.org/2001/XMLSchema-instance"
          }

    root = ET.parse(gmlPath)

    # E1
    element = root.find('//app:AktPlanowaniaPrzestrzennego/app:typPlanu', ns)
    typPlanu = element.attrib['{%s}title' % ns['xlink']].replace('plan','planu')
    metadataElementDict['e1'] = {'e1_lineEdit': "Zbiór danych przestrzennych dla %s <typ_jednostki> <nazwa_jednostki>" % typPlanu}

    # E5
    date = root.find('//app:AktPlanowaniaPrzestrzennego//app:przestrzenNazw', ns)
    metadataElementDict['e5'] = [{'e5_lineEdit': date.text}]

    # E7 - kodowanie z nagłówka GML
    with open(gmlPath, 'r') as file:
        line = file.readlines(1)[0]
        line.replace("'", '"')
        encoding = re.search('encoding="[a-zA-Z0-9\-]{3,10}"', line)[0].split("=")[-1].strip('"').replace(' ', '').replace('-', '').lower()
        if encoding == 'usascii':
            encoding = 'usAscii'
        metadataElementDict['e7'] = [{'e7_cmbbx': encoding}]

    # E9, E10 - słowa kluczowe
    itemsList = []
    date = root.find('//app:AktPlanowaniaPrzestrzennego/app:poziomHierarchii', ns)
    atrybut_title = date.attrib['{%s}title' % ns['xlink']]
    atrybut_href = date.attrib['{%s}href' % ns['xlink']]

    tekst = 'Regionalnym' if atrybut_title == 'regionalny' else 'Lokalne'

    #poziom administracyjny
    itemsList.append({
        'e9_lineEdit': tekst,
        'e10_cmbbx': 'publikacja',
        'e10_dateTimeEdit': QDateTime(2019, 5, 22, 0, 0),
        'e10_lineEdit': 'Zakres przestrzenny',
        'xlink': "http://inspire.ec.europa.eu/metadata-codelist/SpatialScope"
    })

    # poziom jednostki
    itemsList.append({
        'e9_lineEdit': atrybut_title,
        'e10_cmbbx': 'publikacja',
        'e10_dateTimeEdit': QDateTime(2013, 12, 10, 0, 0),
        'e10_lineEdit': 'Poziom planu zagospodarowania przestrzennego',
        'xlink': "http://inspire.ec.europa.eu/codelist/LevelOfSpatialPlanValue"
    })

    # dodanie domyslnych wartosci kluczowych
    itemsList.extend(dictionaries.metadataListWidgetsDefaultItemsDisabled['e9'])
    metadataElementDict['e9'] = itemsList

    # E11
    layer = QgsVectorLayer(gmlPath + '|layername=AktPlanowaniaPrzestrzennego', "gml",  'ogr')
    if layer:
        extent = layer.extent()
        metadataElementDict['e11'] = [{'e11_lineEdit': '%s,%s,%s,%s' % (extent.yMinimum(), extent.yMaximum(), extent.xMinimum(), extent.xMaximum())}]

    # E12
    itemsList = []
    for uklad in root.findall('//*/app:ukladOdniesieniaPrzestrzennego', ns):
        if uklad.text not in itemsList:
            itemsList.append({'e12_cmbbx': uklad.text})
    metadataElementDict['e12'] = itemsList

    # E13
    dates = []
    for date in root.findall('//app:AktPlanowaniaPrzestrzennego/app:poczatekWersjiObiektu', ns):
        dates.append(QDateTime.fromString(date.text, "yyyy-MM-dd'T'hh:mm:ss"))
    oldestDate = utils.oldestQDateTime(dates)
    print('gfdgsdfg', oldestDate)
    if oldestDate is not None:
        metadataElementDict['e13'] = {'e13_dateTimeEdit': oldestDate}

    # E16
    itemsList = []
    for rozdzielczosc in root.findall('//*/app:rozdzielczoscPrzestrzenna', ns):
        if rozdzielczosc.text not in itemsList:
            itemsList.append({'e16_lineEdit': rozdzielczosc.text})
    metadataElementDict['e16'] = itemsList




    return metadataElementDict