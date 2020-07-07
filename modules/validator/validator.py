# -*- coding: utf-8 -*-
import os, datetime
from PyQt5.QtCore import QUrl, QFile, QIODevice
from PyQt5.QtXmlPatterns import QXmlSchema, QXmlSchemaValidator, QAbstractMessageHandler

xsdPath = os.path.join(os.path.dirname(__file__), 'planowaniePrzestrzenne.xsd')
xmlPath = os.path.join(os.path.dirname(__file__),'inv_appExample_pzpw_v001.xml')

from .. import xmlschema
from ..xmlschema.validators.exceptions import XMLSchemaDecodeError
import lxml

class ValidatorXmlSchema:
    """Walidator oparty o bibliotekę zewnętrzną xmlschema - długo wczytuje XSD z internetu - okolo 2 minut """
    def __init__(self):
        start = datetime.datetime.now()
        self.schema = xmlschema.XMLSchema(xsdPath)
        ts = datetime.datetime.now() - start
        print('wczytano XSD w: ', ts.seconds)

    def validateXml(self, xmlPath=xmlPath):
        print('validateXML')
        try:
            self.schema.validate(xmlPath)
            return [True]
        except XMLSchemaDecodeError as error:
            errors = [error.validator, error.obj, error.decoder, error.reason, error.source, error.namespaces]
            return [False, str(errors)]

class ValidatorQXmlSchema:
    """Walidator oparty o bibliotekę Qt5. Ma problemy z wczytaniem XSD - zwraca błąd schematu """
    def __init__(self):
        start = datetime.datetime.now()
        schemaUrl = QUrl.fromLocalFile(xsdPath)
        self.schema = QXmlSchema()
        self.schema.load(schemaUrl)
        ts = datetime.datetime.now() - start
        print('wczytano XSD w: ', ts.seconds)

    def validateXml(self, xmlPath=xmlPath):
        print('validateXML')

        mh = ValidatorQXmlSchema.MessageHandler()

        print('schema')
        if self.schema.isValid():
            file = QFile(xmlPath)
            file.open(QIODevice.ReadOnly)
            validator = QXmlSchemaValidator(self.schema)
            validator.setMessageHandler(mh)
            result = validator.validate(file, QUrl.fromLocalFile(file.fileName()))

            if result:
                return [True]
            else:
                errors = [mh.getMessageType(), mh.getDescription(), mh.getSourceLocation()]
                return [False, str(errors)]
        else:
            print('schema invalid')
            return [False, "blad schematu"]

    class MessageHandler(QAbstractMessageHandler):
        def handleMessage(self, type, description, identifier, sourceLocation):
            self._messageType = type
            self._description = description
            self._sourceLocation = sourceLocation

        def getMessageType(self):
            return self._messageType

        def getDescription(self):
            return self._description

        def getSourceLocation(self):
            return self._description

class ValidatorLxml:
    """Walidator oparty o bibliotekę lxml - wczytuje XSD z internetu 30-40 sekund """
    def __init__(self):
        start = datetime.datetime.now()
        xsd_root = lxml.etree.parse(xsdPath)
        self.schema = lxml.etree.XMLSchema(xsd_root)
        ts = datetime.datetime.now() - start
        print('wczytano XSD w: ', ts.seconds)

    def validateXml(self, xmlPath=xmlPath):
        print('validateXML')

        xml_root = lxml.etree.parse(xmlPath)

        if self.schema.validate(xml_root):
            return [True]
        else:
            return [False, str(self.schema.error_log.filter_from_errors())]
