from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import Qt, QRegExp
import re, os
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

def createFormElementsRysunekAPP():
    """Tworzy listę obiektów klasy 'FormElement'
    na podstawie pliku xsd"""
    xsd = os.path.join(os.path.dirname(__file__), 'validator', 'planowaniePrzestrzenne.xsd')
    formElements = []
    ns = {'glowny': "http://www.w3.org/2001/XMLSchema",
          'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gml': "http://www.opengis.net/gml/3.2",
          'gmlexr': "http://www.opengis.net/gml/3.3/exr"}

    tree = ET.parse(xsd)
    root = tree.getroot()

    complexType = root.find("glowny:complexType[@name='RysunekAktuPlanowniaPrzestrzenegoType']", ns)
    sequence = complexType[0][0][0]  # sekwencja z listą pól
    for element in sequence:
        attrib = element.attrib

        formElement = FormElement(
            name=attrib['name'],
            type=attrib['type']
        )
        # na wypadek braku 'minOccurs'
        try:
            formElement.setMinOccurs(attrib['minOccurs'])
        except KeyError:
            pass
        # documentation
        documentation = element.find("glowny:annotation", ns).find("glowny:documentation", ns)
        formElement.setDocumentation(documentation.text)

        # zdefiniowany w app complextype
        if attrib['type'][:4] == 'app:':
            formElement.markAsComplex()  # ustawia .isComplex = True
            name = str(attrib['type']).replace('Property', '').split(':')[-1]

            complexSequence = root.find("glowny:complexType[@name='%s']" % name, ns)[0]
            for complexElement in complexSequence:
                innerFormElement = FormElement(
                    name=complexElement.attrib['name'],
                    type=complexElement.attrib['type']
                )
                # complex documentation
                complexDocumentation = complexElement.find("glowny:annotation", ns).find("glowny:documentation", ns)
                innerFormElement.setDocumentation(complexDocumentation.text)
                formElement.setInnerFormElement(innerFormElement)

        formElements.append(formElement)

    return formElements

def createFormElementsDokumentFormalny():
    #TODO lista rozwijalna dla atrybutu poziomHierarchii
    """Tworzy listę obiektów klasy 'FormElement'
    na podstawie pliku xsd"""
    xsd = os.path.join(os.path.dirname(__file__),'validator', 'planowaniePrzestrzenne.xsd')
    formElements = []
    ns = {'glowny': "http://www.w3.org/2001/XMLSchema",
          'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gml': "http://www.opengis.net/gml/3.2",
          'gmlexr': "http://www.opengis.net/gml/3.3/exr"}

    tree = ET.parse(xsd)
    root = tree.getroot()

    complexType = root.find("glowny:complexType[@name='DokumentFormalnyType']", ns)
    sequence = complexType[0][0][0]  # sekwencja z listą pól
    for element in sequence:
        attrib = element.attrib
        try:
            formElement = FormElement(
                name=attrib['name'],
                type=attrib['type']
            )
        except:

            elementComplexType = element.find("glowny:complexType", ns)
            elementAttrib = elementComplexType[0][0].attrib
            formElement = FormElement(
                name=attrib['name'],
                type=elementAttrib['base']
            )
        # na wypadek braku 'minOccurs'
        try:
            formElement.setMinOccurs(attrib['minOccurs'])
        except KeyError:
            pass
        # documentation
        documentation = element.find("glowny:annotation", ns).find("glowny:documentation", ns)
        formElement.setDocumentation(documentation.text)

        formElements.append(formElement)

    return formElements

def createFormElementsAktPlanowaniaPrzestrzennego():
    """Tworzy listę obiektów klasy 'FormElement'
    na podstawie pliku xsd"""
    xsd = os.path.join(os.path.dirname(__file__),'validator', 'planowaniePrzestrzenne.xsd')
    formElements = []
    ns = {'glowny': "http://www.w3.org/2001/XMLSchema",
          'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gml': "http://www.opengis.net/gml/3.2",
          'gmlexr': "http://www.opengis.net/gml/3.3/exr"}

    tree = ET.parse(xsd)
    root = tree.getroot()

    complexType = root.find("glowny:complexType[@name='AktPlanowaniaPrzestrzennegoType']", ns)
    sequence = complexType[0][0][0]  # sekwencja z listą pól
    for element in sequence:
        attrib = element.attrib
        try:
            formElement = FormElement(
                name=attrib['name'],
                type=attrib['type']
            )
        except:
            elementComplexType = element.find("glowny:complexType", ns)
            elementAttrib = elementComplexType[0][0].attrib
            formElement = FormElement(
                name=attrib['name'],
                type=elementAttrib['base']
            )
        # na wypadek braku 'minOccurs'
        try:
            formElement.setMinOccurs(attrib['minOccurs'])
        except KeyError:
            pass
        # documentation
        documentation = element.find("glowny:annotation", ns).find("glowny:documentation", ns)
        formElement.setDocumentation(documentation.text)

        formElements.append(formElement)

    return formElements

def layout_widgets(layout):
    """iteracja widgetow wewnątrz layoutu"""
    return (layout.itemAt(i) for i in range(layout.count()))

def getWidgets(layout):
    wtypes = [QPushButton, QLabel, QTextEdit]
    qreg = QRegExp(r'.*')
    mywidgets = {}

    for t in wtypes:
        mywidgets[t] = layout.findChildren(t, qreg)

    for button in mywidgets[QPushButton]:
        print("button:", button.objectName())

    for label in mywidgets[QLabel]:
        print("label:", label.objectName())

def getWidgetsByType(layout, seachObjectType):
    """zwraca listę widgeów danego typu wewnątrz layoutu"""
    qreg = QRegExp(r'.*')
    widgets = layout.findChildren(seachObjectType, qreg)
    return widgets

def getWidgetByName(layout, seachObjectType, name):
    """zwraca widget o zadanym typie i nazwie wewnątrz layoutu"""
    qreg = QRegExp(r'.*')
    widget = layout.findChild(seachObjectType, name)
    return widget
