from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import Qt, QRegExp
from qgis.core import QgsVectorLayer
import re
import os
import itertools
import xml.etree.ElementTree as ET
from .models import FormElement
from . import dictionaries


def showPopup(title, text, icon=QMessageBox.Information):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.Ok)
    return msg.exec_()


def checkZbiorGeometryValidity(gmlFilesPath):
    """sprawdza integralność zbioru APP, czy np. obrysy się nie przecinają"""
    for gmlPath in gmlFilesPath:
        geoms = []
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
            print('------', item)
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


def makeXmlComplex(tag, item, element, formData):
    ComplexItem = ET.SubElement(
        item, element.type.replace('PropertyType', ''))
    # Tworzenie wewnętrzych elementów i wypełnianie ich
    for innerElement in element.innerFormElements:
        innerItem = ET.SubElement(
            ComplexItem, tag+innerElement.name)
        for fd in formData.keys():
            if innerElement.name in fd:
                innerItem.text = formData[fd]
                break
            # else:
                # innerItem.text = 'BRAK DANYCH'


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
        'ukladOdniesieniaPrzestrzennego': dictionaries.ukladyOdniesieniaPrzestrzennego

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
    pomijane_elementy = [
        'plan', 'dokument', 'aktNormatywnyPrzystapienie', 'aktNormatywnyUchwalajacy', 'aktNormatywnyZmieniajacy', 'aktNormatywnyUchylajacy', 'aktNormatywnyUniewazniajacy', 'rysunek', 'przystapienie', 'uchwala', 'zmienia', 'uchyla', 'uniewaznia'
    ]
    # Strefa czasowa timezone jest ustawiona na sztywno
    root_data = {
        'timeStamp': datetime.datetime.utcnow().isoformat()+'Z',
        'numberReturned': "1000000",
        'numberMatched': "unknown",
    }
    # Przestrzenie anzw ustawione na sztywno
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
            else:
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
                                item.set('xlink: href', formData[fd])
                                item.set('xlink:title', formData[fd])

                        elif element.name == 'ukladOdniesieniaPrzestrzennego':
                            slownik = dict_map[element.name]
                            item.text = slownik[formData[fd]]
                        elif element.type == 'date':
                            item.text = formData[fd].toString("yyyy-MM-dd")
                        elif element.type == 'gmd:CI_Date_PropertyType':
                            item.text = formData[fd].toString("yyyy-MM-dd")
                        elif element.type == 'dateTime':
                            item.text = formData[fd].toString(
                                "yyyy-MM-ddThh:mm:ss")
                        else:
                            item.text = formData[fd]
                        break
    return(data)


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


def retrieveFormData(data):
    # TODO Pobierać wartości z qlistwidget zamiast z lineeditów
    # obsługa nillable
    pomijane = ['mapaPodkladowa_lineEdit', 'referencja_lineEdit',
                'aktualnosc_dateTimeEdit', 'lacze_lineEdit', 'lacze_lineEdit_nilReason_chkbx']
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


def createXmlRysunekAPP(layout):
    """Tworzy szablon xml dla Rysunku APP"""
    data = makeXML(docName='RysunekAktuPlanowniaPrzestrzenego',
                   elements=createFormElements(
                       'RysunekAktuPlanowniaPrzestrzenegoType'),
                   formData=retrieveFormData(all_layout_widgets(layout)))

    return data


def createXmlDokumentFormalny(layout):
    """Tworzy szablon xml dla dokumentu formalnego"""
    data = makeXML(docName='DokumentFormalny',
                   elements=createFormElements('DokumentFormalnyType'),
                   formData=retrieveFormData(all_layout_widgets(layout)))

    return data


def createXmlAktPlanowaniaPrzestrzennego(layout, obrysLayer):
    """Tworzy szablon xml dla aktu planowania przestrzennego"""
    data = makeXML(docName='AktPlanowaniaPrzestrzennego',
                   elements=createFormElements(
                       'AktPlanowaniaPrzestrzennegoType'),
                   formData=retrieveFormData(all_layout_widgets(layout)),
                   obrysLayer=obrysLayer)

    return data
