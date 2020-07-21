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
                innerWidgets = all_layout_widgets(layout=widget.widget().layout())
                allWidgets.extend(innerWidgets)
            elif isinstance(widget, QGroupBox):
                innerWidgets = all_layout_widgets(layout=widget.layout())
                allWidgets.extend(innerWidgets)
            else:   # zwykly widget
                allWidgets.append(widget)
        elif isinstance(item, QSpacerItem):
            pass
        else:
            print('------',item)
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
