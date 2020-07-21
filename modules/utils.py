from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import Qt, QRegExp
import re
import os
import xml.etree.ElementTree as ET
from .models import FormElement


def showPopup(title, text, icon=QMessageBox.Information):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.Ok)
    return msg.exec_()


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


def makeXML(docName, elements, IPP='PL.ZIPPZP.9999_14-PZPW_P1_20200525'):
    import datetime

    # Układ współrzędnych na sztywno
    srsName = 'http://www.opengis.net/def/crs/EPSG/0/2180'

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
    item.set('CodeSpace', codeSpace)
    item.text = '/'.join([codeSpace, docName, IPP.replace('_', '/')])

    for element in elements:
        if 'ReferenceType' not in element.type:
            item = ET.SubElement(items, tag + element.name)
            if element.isComplex() == True:
                ComplexItem = ET.SubElement(item, element.type[4:])
                for innerElement in element.innerFormElements:
                    innerItem = ET.SubElement(
                        ComplexItem, tag+innerElement.name)
                    innerItem.text = 'placeholder'
            elif element.name == 'zasiegPrzestrzenny':
                subItem1 = ET.SubElement(item, 'gml:MultiSurface')
                subItem1.set('srsDimention', '2')
                subItem1.set('srsName', srsName)
                subItem2 = ET.SubElement(subItem1, 'gml:surfaceMember')
                subItem3 = ET.SubElement(subItem2, 'gml:Polygon')
                subItem4 = ET.SubElement(subItem3, 'gml:exterior')
                subItem5 = ET.SubElement(subItem4, 'gml:LinearRing')
                subItem6 = ET.SubElement(subItem5, 'gml:posList')
                coord = '256000.0 686000.0 325000.0 350000.0 745000.0 240000.0 450000.0 431000.0'
                subItem6.text = coord

            else:
                item.text = 'placeholder'
    return(data)


def createXmlRysunekAPP():
    """Tworzy szablon xml dla Rysunku APP"""
    data = makeXML(docName='RysunekAktuPlanowniaPrzestrzenego',
                   elements=createFormElements('RysunekAktuPlanowniaPrzestrzenegoType'))

    return data


def createXmlDokumentFormalny():
    """Tworzy szablon xml dla dokumentu formalnego"""
    data = makeXML(docName='DokumentFormalny',
                   elements=createFormElements('DokumentFormalnyType'))

    return data


def createXmlAktPlanowaniaPrzestrzennego():
    """Tworzy szablon xml dla aktu planowania przestrzennego"""
    data = makeXML(docName='AktPlanowaniaPrzestrzennego',
                   elements=createFormElements('AktPlanowaniaPrzestrzennegoType'))

    return data
