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
            errors = []
            errors.append(error.validator)
            errors.append(error.obj)
            errors.append(error.decoder)
            errors.append(error.reason)
            errors.append(error.source)
            errors.append(error.namespaces)
            return [False, errors]

class ValidatorQXmlSchema:

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
                errors = []
                errors.append(mh.getMessageType())
                errors.append(mh.getDescription())
                errors.append(mh.getSourceLocation())
                return [False, errors]
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
            return [False,self.schema.error_log.filter_from_errors()]
