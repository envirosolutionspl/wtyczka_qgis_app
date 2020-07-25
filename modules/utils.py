from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import Qt, QRegExp
from qgis.core import QgsVectorLayer
import re
import os
import itertools
import xml.etree.ElementTree as ET
from .models import FormElement
from . import dictionaries
import datetime


def showPopup(title, text, icon=QMessageBox.Information):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.Ok)
    return msg.exec_()


def isAppOperative(gmlPath):
    """sprawdza czy zbiór APP jest obowiązującym zbiorem"""
    # TODO: sprawdzenie odpowiedniego elementu GML
    return True


def checkZbiorGeometryValidity(gmlFilesPath):
    """sprawdza integralność zbioru APP, czy np. obrysy się nie przecinają
    na podstawie listy ścieżek do plików GML"""
    geoms = []
    for gmlPath in gmlFilesPath:
        if isAppOperative(gmlPath):  # jest obowiązujący
            layer = QgsVectorLayer(gmlPath, "", 'ogr')
            if not layer.isValid():
                return [False, "Niepoprawna warstwa wektorowa w pliku %s" % gmlPath]
            if not layer.featureCount():
                return [False, "Brak obiektów przestrzennych w warstwie %s" % gmlPath]
            feat = next(layer.getFeatures())
            geoms.append((feat.geometry(), gmlPath))
    for a, b in itertools.combinations(geoms, 2):
        geom1 = a[0]
        path1 = a[1]
        geom2 = b[0]
        path2 = b[1]
        if geom1.overlaps(geom2):
            return [False, "Geometrie swóch APP w ramach jednego zbioru nie mogą na siebie nachodzić. Dotyczy plików\n\n%s\n%s" % (path1, path2)]
    return [True]


def getNamespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''


def createFormElements(attribute):
    """Tworzy listę obiektów klasy 'FormElement'
    na podstawie pliku xsd"""

    xsd = os.path.join(os.path.dirname(__file__),
                       'validator', 'planowaniePrzestrzenne.xsd')

    ns = {'glowny': "http://www.w3.org/2001/XMLSchema",
          'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gml': "http://www.opengis.net/gml/3.2",
          'gmlexr': "http://www.opengis.net/gml/3.3/exr"}
    formElements = []

    tree = ET.parse(xsd)
    root = tree.getroot()

    complexType = root.find(
        "glowny:complexType[@name='" + attribute + "']", ns)
    sequence = complexType[0][0][0]  # sekwencja z listą pól
    for element in sequence:
        attrib = element.attrib

        try:
            elementType = attrib['type']
            formElement = FormElement(
                name=attrib['name'],
                type=elementType,
                form=attribute
            )
        except KeyError:
            elementComplexType = element.find("glowny:complexType", ns)
            elementAttrib = elementComplexType[0][0].attrib
            elementType = elementAttrib['base']
            formElement = FormElement(
                name=attrib['name'],
                type=elementType,
                form=attribute
            )
            try:  # gdy jest nillable
                if element.attrib['nillable'] == 'true':
                    formElement.setNillable()
            except KeyError:  # gdyby nie bylo rowniez nillable
                pass

        # na wypadek braku 'minOccurs'
        try:
            formElement.setMinOccurs(attrib['minOccurs'])
        except KeyError:
            pass
        # na wypadek braku 'maxOccurs'
        try:
            formElement.setMaxOccurs(attrib['maxOccurs'])
        except KeyError:
            pass
        # documentation
        documentation = element.find("glowny:annotation", ns).find(
            "glowny:documentation", ns)
        formElement.setDocumentation(documentation.text)

        # zdefiniowany w app complextype
        # if elementType == 'app:IdentyfikatorPropertyType':
        if elementType[:4] == 'app:':
            formElement.markAsComplex()  # ustawia .isComplex = True
            name = str(elementType).replace('Property', '').split(':')[-1]

            complexSequence = root.find(
                "glowny:complexType[@name='%s']" % name, ns)[0]
            for complexElement in complexSequence:
                try:    # jeżeli jest atrybut 'type'
                    innerFormElement = FormElement(
                        name=complexElement.attrib['name'],
                        type=complexElement.attrib['type'],
                        form=attribute
                    )
                except KeyError:    # jeżeli nie ma atrybutu 'type'
                    innerFormElement = FormElement(
                        name=complexElement.attrib['name'],
                        type="anyURI",
                        form=attribute
                    )
                    try:  # gdy jest nillable
                        if complexElement.attrib['nillable'] == 'true':
                            innerFormElement.setNillable()
                    except KeyError:  # gdyby nie bylo rowniez nillable
                        pass
                # complex documentation
                complexDocumentation = complexElement.find(
                    "glowny:annotation", ns).find("glowny:documentation", ns)
                innerFormElement.setDocumentation(complexDocumentation.text)
                formElement.setInnerFormElement(innerFormElement)

        formElements.append(formElement)

    return formElements


def createFormElementsRysunekAPP():
    """Tworzy listę obiektów klasy 'FormElement'
    na podstawie pliku xsd dla Rysunku APP"""

    return createFormElements('RysunekAktuPlanowniaPrzestrzenegoType')


def createFormElementsDokumentFormalny():
    """Tworzy listę obiektów klasy 'FormElement'
    na podstawie pliku xsd dla Rysunku APP"""

    return createFormElements('DokumentFormalnyType')


def createFormElementsAktPlanowaniaPrzestrzennego():
    """Tworzy listę obiektów klasy 'FormElement'
    na podstawie pliku xsd dla Rysunku APP"""

    return createFormElements('AktPlanowaniaPrzestrzennegoType')


def layout_widgets(layout):
    """lista widgetow/layoutow wewnątrz layoutu"""
    return (layout.itemAt(i) for i in range(layout.count()))


def layout_widget_by_name(layout, name):
    """wyszukuje widgeta wedlug nazwy wewnatrz layoutu
    Do wykorystania również w trakcie tworzenia layoutu (np. QHBoxLayout)"""
    for item in layout_widgets(layout):
        if isinstance(item, QLayout):   # zagnieżdzony layout
            result = layout_widget_by_name(layout=item, name=name)
            if result:
                return result
        elif isinstance(item, QWidgetItem):
            widget = item.widget()
            # print(widget.objectName())
            if name == widget.objectName():
                return widget
        else:
            raise NotImplementedError


def all_layout_widgets(layout):
    """lista wszystkich widgetow/layoutow wewnątrz layoutu uwzględniając zagnieżdzone elementy"""
    types = [QLineEdit, QLabel, QComboBox, QCheckBox, QDateEdit, QListWidget]
    allWidgets = []
    for item in layout_widgets(layout):
        if isinstance(item, QLayout):   # zagnieżdzony layout
            innerWidgets = all_layout_widgets(layout=item)
            allWidgets.extend(innerWidgets)
        elif isinstance(item, QWidgetItem):
            widget = item.widget()
            if isinstance(widget, QScrollArea):
                innerWidgets = all_layout_widgets(
                    layout=widget.widget().layout())
                allWidgets.extend(innerWidgets)
            elif isinstance(widget, QGroupBox):
                innerWidgets = all_layout_widgets(layout=widget.layout())
                allWidgets.extend(innerWidgets)
            else:   # zwykly widget
                allWidgets.append(widget)
        elif isinstance(item, QSpacerItem):
            pass
        else:
            raise NotImplementedError
    return allWidgets


def getWidgets(layout, types=[QPushButton, QLabel, QTextEdit, QLineEdit, QDateEdit]):
    wtypes = types
    qreg = QRegExp(r'.*')
    mywidgets = {}

    for t in wtypes:
        mywidgets[t] = layout.findChildren(t, qreg)
    return(mywidgets)


def getWidgetsByType(layout, searchObjectType):
    """zwraca listę widgeów danego typu wewnątrz layoutu"""
    qreg = QRegExp(r'.*')
    widgets = layout.findChildren(searchObjectType, qreg)
    return widgets


def getWidgetByName(layout, searchObjectType, name):
    """zwraca widget o zadanym typie i nazwie wewnątrz layoutu statycznego
    (np. wewnątrz całego okna formularza
    Do wykorzystania gdy już są zbudowane formularze/widoki"""
    widget = layout.findChild(searchObjectType, name)
    return widget


def makeXmlComplex(tag, item, element):
    ComplexItem = ET.SubElement(
        item, element.type.replace('PropertyType', ''))
    for inner in element.innerFormElements:
        subItem = ET.SubElement(ComplexItem, tag + inner.name)
        subItem.text = inner.refObject.text()


# def makeXmlListComplex(tag, item, element, formData):
#     # Tworzenie wewnętrzych elementów i wypełnianie ich
#     for fee in formData:
#         ComplexItem = ET.SubElement(
#             item, element.type.replace('PropertyType', ''))
#         for innerElement in element.innerFormElements:
#             innerItem = ET.SubElement(
#                 ComplexItem, tag+innerElement.name)
#             for fd in fee.keys():
#                 if innerElement.name in fd:
#                     innerItem.text = fee[fd]
#                     break
#             # else:
#                 # innerItem.text = 'BRAK DANYCH'


def makeXmlListElements(tag, item, element, formData, slownik={}):
    # Tworzenie wewnętrzych elementów i wypełnianie ich
    nilReason = ["inapplicable", "missing", "template", "unknown", "withheld"]
    for fee in formData:
        if element.isComplex():
            ComplexItem = ET.SubElement(
                item, element.type.replace('PropertyType', ''))
            for innerElement in element.innerFormElements:
                innerItem = ET.SubElement(
                    ComplexItem, tag+innerElement.name)
                for fd in fee.keys():

                    try:  # Sprawdzanie Nil == True
                        if fee[innerElement.name+'_lineEdit_nilReason_chkbx']:
                            makeNil(
                                innerItem, innerElement, nilReason[fee[innerElement.name+'_lineEdit_nilReason_cmbbx']])  # fee[innerElement.name+'_lineEdit_nilReason_cmbbx'])
                    except:
                        pass

                    if innerElement.name in fd:
                        innerItem.text = fee[fd]
                        break
        else:
            multiItem = ET.SubElement(
                item, tag+element.name)
            for fd in fee.keys():
                try:  # Sprawdzanie Nil == True
                    if fee[innerElement.name+'_lineEdit_nilReason_chkbx']:
                        makeNil(
                            innerItem, innerElement, fee[innerElement.name+'_lineEdit_nilReason_cmbbx'])
                except:
                    pass
                if element.name in fd:
                    multiItem.text = fee[fd]
                    break


def make_polygon(polygons):
    BoundaryList = []
    # pierwszy poligon jest outerBoundary, kolejne innerBoundary
    for polygon in polygons:
        Boundary = ''
        for x, y in polygon:
            Boundary = ' '.join([Boundary, "{} {}".format(x, y)])
        BoundaryList.append(Boundary[1:])
    return(BoundaryList)


def getCoordinates(obrysLayer):
    CoordinatesList = []
    coordinates = ''
    for f in obrysLayer.getFeatures():
        obrys = f.geometry()
    # getGeometry - wystąpił przypadek zmiany id, getFeatures jest bezpieczniejsze
    # obrys = obrysLayer.getGeometry(1)
    if obrys.isMultipart():
        for poligon in obrys.asMultiPolygon():
            CoordinatesList.append(make_polygon(poligon))
    else:
        # Poligon, który został multipoligonem utrzymuje typ multipoligona nawet jako zwykły poligon
        CoordinatesList.append(make_polygon(obrys.asPolygon()))
    return CoordinatesList


def makeSpatialExtent(node, CoordinatesList):
    for polygon in CoordinatesList:
        isBoundary = True  # 0 - True, >0 - False
        subItem2 = ET.SubElement(node, 'gml:surfaceMember')
        subItem3 = ET.SubElement(subItem2, 'gml:Polygon')
        for coordinates in polygon:
            if isBoundary == True:
                subItem4 = ET.SubElement(subItem3, 'gml:exterior')
            else:
                subItem4 = ET.SubElement(subItem3, 'gml:interior')
            subItem5 = ET.SubElement(subItem4, 'gml:LinearRing')
            subItem6 = ET.SubElement(subItem5, 'gml:posList')
            subItem6.text = coordinates
            isBoundary = False


def makeXML(docName, elements, formData, obrysLayer=None):
    # TODO Dodać obsługę nillable: https://inspire.ec.europa.eu/forum/discussion/view/61478/contents-of-attribute-nilreason-eg-unknown-vs-httpinspireeceuropaeucodelistvoidreasonvalueunknown
    # TODO Dodać iterację po obiektach z licznością *
    import datetime
    dict_map = {
        'status': dictionaries.statusListaKodowa,
        'poziomHierarchii': dictionaries.poziomyHierarchii,
        'nilReason': dictionaries.nilReasons,
        'zasiegPrzestrzenny': dictionaries.ukladyOdniesieniaPrzestrzennego,
        'typPlanu': dictionaries.typyPlanu,
        'dziennikUrzedowy': dictionaries.dziennikUrzedowyKod,
        'ukladOdniesieniaPrzestrzennego': dictionaries.ukladyOdniesieniaPrzestrzennego,
        'data': dictionaries.cI_DateTypeCode
    }
    IPP = formData['idIIP_lineEdit']
    if obrysLayer != None:
        CoordinatesList = getCoordinates(obrysLayer)
        epsg = str(obrysLayer.crs().authid()).split(':')[1]
        # Układ współrzędnych
        for crs in dict_map['ukladOdniesieniaPrzestrzennego'].values():
            if epsg in crs:
                srsName = crs
            else:
                # TODO co w przypadku, gdy CRS jest inny niż w słowniku - rozwiązanie tymczasowe
                srsName = "http://www.opengis.net/def/crs/EPSG/0/2180"
    else:
        CoordinatesList = None

    # Elementy, których wartości nie ma w formularzu
    pomijane_elementy = formSkippedElements(docName)

    # Strefa czasowa timezone jest ustawiona na sztywno
    root_data = {
        'timeStamp': datetime.datetime.utcnow().isoformat()+'Z',
        'numberReturned': "1000000",
        'numberMatched': "unknown",
    }
    # Przestrzenie nazw ustawione na sztywno
    namespaces = {
        'xmlns:gco': "http://www.isotc211.org/2005/gco",
        'xmlns:gmd': "http://www.isotc211.org/2005/gmd",
        'xmlns:gml': "http://www.opengis.net/gml/3.2",
        'xmlns:wfs': "http://www.opengis.net/wfs/2.0",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xmlns:app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'xsi:schemaLocation': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0 ../appSchema/appSchema_app_v0_0_1/planowaniePrzestrzenne.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd"
    }
    # create the file structure
    data = ET.Element('wfs:FeatureCollection')
    datamember = ET.SubElement(data, 'wfs:member')

    for rd in root_data.keys():
        data.set(rd, root_data[rd])

    for ns in namespaces.keys():
        data.set(ns, namespaces[ns])

    tag = 'app:'
    items = ET.SubElement(datamember, tag + docName)
    items.set('gml:id', IPP)
    item = ET.SubElement(items, 'gml:identifier')
    codeSpace = 'http://zagospodarowanieprzestrzenne.gov.pl/app'
    item.set('codeSpace', codeSpace)
    item.text = '/'.join([codeSpace, docName, IPP.replace('_', '/')])

    for element in elements:
        if element.name not in pomijane_elementy:
            # if 'ReferenceType' not in element.type:
            item = ET.SubElement(items, tag + element.name)
            # Tworzenie wewnętrzego elementu obiektu złożonego
            if element.isComplex() == True:
                for fd in formData.keys():
                    if element.name in fd:
                        if type(formData[fd]) == list:
                            for params in formData[fd]:
                                makeXmlComplex(tag, item, element, params)
                        else:
                            makeXmlComplex(tag, item, element, formData)

            elif element.name == 'zasiegPrzestrzenny':
                subItem1 = ET.SubElement(item, 'gml:MultiSurface')
                subItem1.set('srsDimension', '2')
                subItem1.set('srsName', srsName)
                makeSpatialExtent(subItem1, CoordinatesList)
            else:  # Tworzenie elementów elementarnych
                for fd in formData.keys():
                    if element.name in fd:
                        if 'ReferenceType' in element.type:
                            slownik = dict_map[element.name]
                            try:
                                # TODO Sprawdzić dla wszystkich formularzy
                                if element.name == 'typPlanu':
                                    link = 'http://zagospodarowanieprzestrzenne.gov.pl/codelist/AktPlanowaniaPrzestrzennegoKod/'
                                elif element.name == 'dziennikUrzedowy':
                                    link = 'http://zagospodarowanieprzestrzenne.gov.pl/codelist/DziennikUrzedowyKod/'
                                else:
                                    link = ''
                                if 'http' in (link+slownik[formData[fd]]):
                                    item.set(
                                        'xlink:href', (link+slownik[formData[fd]]))
                                    item.set('xlink:title', formData[fd])
                            except:
                                item.set('xlink:href', formData[fd])
                                item.set('xlink:title', formData[fd])

                        elif element.name == 'ukladOdniesieniaPrzestrzennego':
                            slownik = dict_map[element.name]
                            item.text = slownik[formData[fd]]
                        elif element.type == 'date':
                            item.text = formData[fd].toString("yyyy-MM-dd")
                        elif element.type == 'gmd:CI_Date_PropertyType':
                            slownik = dict_map[element.name]
                            item1 = ET.SubElement(item, 'gml:CI_Date')
                            item2 = ET.SubElement(item1, 'gml:date')
                            item3 = ET.SubElement(item2, 'gco:Date')
                            item3.text = formData[fd].toString("yyyy-MM-dd")
                            # item4 = ET.SubElement(item2, 'gmd:DateType')
                            # item5 = ET.SubElement(item4, 'gmd:CI_DateTypeCode')
                            # item5.set(
                            #     'codeList', 'http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_DateTypeCode')
                            # item5.set('codeListValue', slownik[formData[fd]])
                            # item5.text = formData[fd]
                        elif element.type == 'dateTime':
                            item.text = formData[fd].toString(
                                "yyyy-MM-ddThh:mm:ss")
                        else:
                            item.text = formData[fd]
                        break
    return(data)


def formSkippedElements(docName):
    """Zwraca listę atrybutów dla poszczególnego dokumentu, które nie występują w formularzu"""
    pomijane = []
    if docName == 'AktPlanowaniaPrzestrzennego':
        pomijane = ['dokument', 'aktNormatywnyPrzystapienie', 'aktNormatywnyUchwalajacy',
                    'aktNormatywnyZmieniajacy', 'aktNormatywnyUchylajacy', 'aktNormatywnyUniewazniajacy', 'rysunek']
    elif docName == 'RysunekAktuPlanowniaPrzestrzenego':
        pomijane = ['plan']
    elif docName == 'DokumentFormalny':
        pomijane = ['przystapienie', 'uchwala',
                    'zmienia', 'uchyla', 'uniewaznia']
    return(pomijane)


def formSkippedObjects(docName):
    """Zwraca listę nazw obiektów edytowalnych w formularzu, które nie podlegają umieszczeniu w xml"""
    pomijane = []
    if docName == 'AktPlanowaniaPrzestrzennego':
        pomijane = ['mapaPodkladowa_lineEdit', 'referencja_lineEdit',
                    'aktualnosc_dateTimeEdit', 'lacze_lineEdit', 'lacze_lineEdit_nilReason_chkbx']
    elif docName == 'RysunekAktuPlanowniaPrzestrzenego':
        pomijane = []
    elif docName == 'DokumentFormalny':
        pomijane = []
    return(pomijane)


def checkForNillable(fe, element):
    nil = False  # Brak Nillable
    if fe.isNillable:
        widgets = all_layout_widgets(element[1])
        for widget in widgets:
            if type(widget).__name__ == 'QCheckBox':
                if widget.isChecked() == True:
                    nil = True
    return nil


def checkElement(fe, element):

    try:  # LineEdit / Date
        # print('1' + element.text())
        if fe.minOccurs > 0 and (element.text() is None or element.text() == 'NULL' or element.text() == ''):
            # try:
            #     if checkForNillable(fe, element):
            #         return(checkForNillable(fe, element))
            # except:
            #     pass
            showPopup(title='Błąd formularza',
                      text='Brak wartości dla atrybutu: %s' % fe.name)
            return False
    except:  # Combobox
        try:
            # print('2' + element.currentText())
            if fe.minOccurs > 0 and (element.currentText() is None or element.currentText() == ''):
                # try:
                #     if checkForNillable(fe, element):
                #         return(checkForNillable(fe, element))
                # except:
                #     pass
                showPopup(title='Błąd formularza',
                          text='Brak wartości dla atrybutu: %s' % fe.name)
                return False
        except:
            try:  # ListWidget
                # print('3')
                if fe.minOccurs > 0 and element.count() > 0:
                    # try:
                    #     if checkForNillable(fe, element):
                    #         return(checkForNillable(fe, element))
                    # except:
                    #     pass
                    showPopup(title='Błąd formularza',
                              text='Brak wartości dla atrybutu: %s' % fe.name)
                    return False
            except:
                print('checkElement')
    return True


def isFormFilled(dialog):
    for fe in dialog.formElements:
        if fe.name in dialog.pomijane:
            continue
        # Sprawdza tylko czy wartość występuje co najmniej raz - brak specyfikacji dokładnej liczności
        if type(fe.refObject) == list:
            for element in fe.refObject:
                if checkElement(fe, element) == False:  # Brak wartości
                    return False
        elif fe.refNilObject is not None:
            print(fe.name)
            widgets = all_layout_widgets(fe.refNilObject)
            for widget in widgets:
                if type(widget).__name__ == 'QCheckBox':
                    if widget.isChecked() == True:
                        return True
            if checkElement(fe, fe.refObject) == False:  # Brak wartości
                return False
        else:
            if checkElement(fe, fe.refObject) == False:  # Brak wartości
                return False
    return True  # Wszystko wypełnione


def getListWidgetItems(element):
    itemList = []
    for i in range(element.count()):
        item = element.item(i).data(Qt.UserRole)
        for key in item.keys():
            if type(item[key]) == str or type(item[key]) == int:
                continue
            else:
                item[key] = item[key].toString("yyyy-MM-ddThh:mm:ss")
        itemList.append(item)
    return(itemList)

# def findFormObject


def retrieveFormData(elements, data, pomijane):

    form_data = {}
    for el in data:

        if el.objectName() in pomijane:
            continue
        if 'lineEdit' in el.objectName():
            try:
                form_data[el.objectName()] = el.text()
            except:
                if 'ComboBox' in type(el).__name__:
                    form_data[el.objectName()] = el.currentText()
        elif 'dateTimeEdit' in el.objectName():
            try:
                form_data[el.objectName()] = el.dateTime()
            except:
                if 'ComboBox' in type(el).__name__:
                    form_data[el.objectName()] = el.currentText()
        elif 'listWidget' in el.objectName():
            form_data[el.objectName()] = getListWidgetItems(el)
        else:
            try:
                if 'ComboBox' in type(el).__name__:
                    form_data[el.objectName()] = el.currentText()
            except:
                continue
    return(form_data)


def getListWidgetItems(listWidget):
    itemList = []
    for i in range(listWidget.count()):
        item = listWidget.item(i).data(Qt.UserRole)
        # print(item)
        for key in item.keys():
            if type(item[key]) == str or type(item[key]) == int:
                continue
            elif type(item[key]) == bool:
                continue
            else:
                item[key] = item[key].toString("yyyy-MM-ddThh:mm:ss")
        itemList.append(item)
    return(itemList)


def makeMapaPodkladowaNode(item, data):
    for i in data.keys():
        item1 = ET.SubElement(item, 'app:MapaPodkladowa')
        item1.text = data[i]


def makeListWidgetLaczeNode(item, data):
    for i in data.keys():
        item1 = ET.SubElement(item, 'app:lacze')
        item1.text = data[i]


def makeDataNode(item, data, slownik):
    item1 = ET.SubElement(item, 'gml:CI_Date')
    item2 = ET.SubElement(item1, 'gml:date')
    item3 = ET.SubElement(item2, 'gco:Date')
    item3.text = data[0].dateTime().toString("yyyy-MM-dd")
    item4 = ET.SubElement(item2, 'gmd:DateType')
    item5 = ET.SubElement(item4, 'gmd:CI_DateTypeCode')
    item5.set(
        'codeList', 'http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_DateTypeCode')
    item5.set('codeListValue', slownik[data[1].currentText()])
    item5.text = data[1].currentText()


def makeNil(item, element, nilReason):
    if element.isNillable:
        item.set('nilReason', str(nilReason))
        item.set('xsi:nil', 'true')


def checkForNoValue(element):
    try:
        if element.text() == '' or element.text() == 'NULL':
            return True
        # print(element.text())
    except:
        try:
            if element.currentText() == '':
                return True
            # print(element.currentText())
        except:
            try:
                params = getListWidgetItems(element)
                if params == []:
                    return True
            except:
                # print(element)
                pass
    return False  # jest wartość


def createXmlData(dialog, obrysLayer):  # NOWE

    dict_map = {
        'status': dictionaries.statusListaKodowa,
        'poziomHierarchii': dictionaries.poziomyHierarchii,
        'nilReason': dictionaries.nilReasons,
        'zasiegPrzestrzenny': dictionaries.ukladyOdniesieniaPrzestrzennego,
        'typPlanu': dictionaries.typyPlanu,
        'dziennikUrzedowy': dictionaries.dziennikUrzedowyKod,
        'ukladOdniesieniaPrzestrzennego': dictionaries.ukladyOdniesieniaPrzestrzennego,
        'data': dictionaries.cI_DateTypeCode
    }

    docNames = {
        'RasterFormularzDialog': 'RysunekAktuPlanowniaPrzestrzenego',
        'WektorFormularzDialog': 'AktPlanowaniaPrzestrzennego',
        'DokumentyFormularzDialog': 'DokumentFormalny'
    }

    docName = docNames[type(dialog).__name__]
    try:
        CoordinatesList = getCoordinates(obrysLayer)
        epsg = str(obrysLayer.crs().authid()).split(':')[1]
        # Układ współrzędnych
        for crs in dict_map['ukladOdniesieniaPrzestrzennego'].values():
            if epsg in crs:
                srsName = crs
            else:
                # TODO WYJĄTEK/POPUP DLA INNYCH CRS
                # TODO co w przypadku, gdy CRS jest inny niż w słowniku - rozwiązanie tymczasowe
                srsName = "http://www.opengis.net/def/crs/EPSG/0/"+epsg
    except:
        CoordinatesList = None

    # Strefa czasowa timezone jest ustawiona na sztywno
    root_data = {
        'timeStamp': datetime.datetime.utcnow().isoformat()+'Z',
        'numberReturned': "1000000",
        'numberMatched': "unknown",
    }

    # Przestrzenie nazw ustawione na sztywno
    namespaces = {
        'xmlns:gco': "http://www.isotc211.org/2005/gco",
        'xmlns:gmd': "http://www.isotc211.org/2005/gmd",
        'xmlns:gml': "http://www.opengis.net/gml/3.2",
        'xmlns:wfs': "http://www.opengis.net/wfs/2.0",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xmlns:app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
        'xsi:schemaLocation': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0 ../appSchema/appSchema_app_v0_0_1/planowaniePrzestrzenne.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd"
    }
    # create the file structure
    data = ET.Element('wfs:FeatureCollection')
    datamember = ET.SubElement(data, 'wfs:member')

    for rd in root_data.keys():
        data.set(rd, root_data[rd])

    for ns in namespaces.keys():
        data.set(ns, namespaces[ns])

    tag = 'app:'
    items = ET.SubElement(datamember, tag + docName)

    itemid = ET.SubElement(items, 'gml:identifier')
    codeSpace = 'http://zagospodarowanieprzestrzenne.gov.pl/app'
    itemid.set('codeSpace', codeSpace)

    for fe in dialog.formElements:
        refObject = fe.refObject

        if checkForNoValue(refObject):
            continue
        if fe.name in dialog.pomijane and fe.name != 'zasiegPrzestrzenny':
            continue
        if fe.name in dict_map.keys():
            slownik = dict_map[fe.name]  # sprawdzać też na innerElements
        if fe.name == 'typPlanu':
            link = 'http://zagospodarowanieprzestrzenne.gov.pl/codelist/AktPlanowaniaPrzestrzennegoKod/'
        elif fe.name == 'dziennikUrzedowy':
            link = 'http://zagospodarowanieprzestrzenne.gov.pl/codelist/DziennikUrzedowyKod/'
        else:
            link = ''
        if fe.name == 'idIIP':
            IIP = refObject.text()
            items.set('gml:id', IIP)
            itemid.text = '/'.join([codeSpace, docName, IIP.replace('_', '/')])

        print(fe.name)

        if fe.isComplex():
            item = ET.SubElement(items, tag + fe.name)
            if fe.maxOccurs == 'unbounded':  # Element jest wielokrotny
                params = getListWidgetItems(refObject)
                # print(params)
                makeXmlListElements(tag, item, fe, params)
                continue
            else:
                makeXmlComplex(tag, item, fe)
                continue
        elif fe.maxOccurs == 'unbounded':  # Element jest wielokrotny
            params = getListWidgetItems(refObject)
            if params == [] and fe.minOccurs == 0:
                continue
            makeXmlListElements(tag, items, fe, params)
            continue
        else:  # Element jest elementarny
            item = ET.SubElement(items, tag + fe.name)

        if fe.isNillable:
            refNilObject = fe.refNilObject
            nil = False
            widgets = all_layout_widgets(refNilObject)
            for widget in widgets:
                if type(widget).__name__ == 'QCheckBox':
                    if widget.isChecked() == True:
                        nil = True
                        for widget in widgets:
                            if type(widget).__name__ == 'QComboBox':
                                makeNil(item, fe, widget.currentText())
                                continue

        if fe.name == 'data':
            makeDataNode(item, refObject, slownik)
        elif fe.name == 'ukladOdniesieniaPrzestrzennego':
            item.text = slownik[refObject.currentText()]
        elif fe.type == 'date':
            item.text = refObject.dateTime().toString("yyyy-MM-dd")
        elif fe.type == 'dateTime':
            item.text = refObject.dateTime().toString(
                "yyyy-MM-ddThh:mm:ss")
        elif 'ReferenceType' in fe.type:
            try:
                item.set('xlink:href', (link+slownik[refObject.text()]))
                item.set('xlink:title', refObject.text())
            except:
                item.set('xlink:href',
                         (link+slownik[refObject.currentText()]))
                item.set('xlink:title', refObject.currentText())
        elif fe.name == 'zasiegPrzestrzenny':
            subItem1 = ET.SubElement(item, 'gml:MultiSurface')
            subItem1.set('srsDimension', '2')
            subItem1.set('srsName', srsName)
            makeSpatialExtent(subItem1, CoordinatesList)
        else:
            try:
                item.text = refObject.text()
            except:
                try:
                    item.text = refObject.currentText()
                except:
                    pass

    return data


def createXmlRysunekAPP(layout):
    """Tworzy szablon xml dla Rysunku APP"""
    docName = 'RysunekAktuPlanowniaPrzestrzenego'
    elements = createFormElements(docName+'Type')
    data = makeXML(docName=docName,
                   elements=elements,
                   formData=retrieveFormData(
                       elements,
                       all_layout_widgets(layout),
                       formSkippedObjects(docName)))

    return data


def createXmlDokumentFormalny(layout):
    """Tworzy szablon xml dla dokumentu formalnego"""
    docName = 'DokumentFormalny'
    elements = createFormElements(docName+'Type')
    data = makeXML(docName=docName,
                   elements=elements,
                   formData=retrieveFormData(
                       elements,
                       all_layout_widgets(layout),
                       formSkippedObjects(docName)))

    return data


def createXmlAktPlanowaniaPrzestrzennego(layout, obrysLayer):
    """Tworzy szablon xml dla aktu planowania przestrzennego"""
    docName = 'AktPlanowaniaPrzestrzennego'
    elements = createFormElements(docName+'Type')
    data = makeXML(docName=docName,
                   elements=elements,
                   formData=retrieveFormData(
                       elements,
                       all_layout_widgets(layout),
                       formSkippedObjects(docName)),
                   obrysLayer=obrysLayer)

    return data
