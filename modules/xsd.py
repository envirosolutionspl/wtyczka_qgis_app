# -*- coding: utf-8 -*-
import os, datetime
from PyQt5.QtCore import QUrl, QFile, QIODevice
from PyQt5.QtXmlPatterns import QXmlSchema, QXmlSchemaValidator, QAbstractMessageHandler

from .utils import getNamespace
from . import xmlschema
from .xmlschema.validators.exceptions import XMLSchemaDecodeError

xsdPath = os.path.join(os.path.dirname(__file__), 'planowaniePrzestrzenne.xsd')
# xsdPath = os.path.join(os.path.dirname(__file__), 'KlienciOrders.xsd')
xmlPath = os.path.join(os.path.dirname(__file__), 'inv_appExample_pzpw_v001.xml')
# xmlPath = os.path.join(os.path.dirname(__file__), 'invKlienciOrders.xml')


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


def validateXml(xmlPath=xmlPath, xsdPath=xsdPath):
    print('validateXML')
    startTime = datetime.datetime.now()
    try:
        xmlschema.validate(xmlPath, xsdPath)
        print('brak błędu')
        stopTime = datetime.datetime.now()
    except XMLSchemaDecodeError as error:
        print("błąd:\n")
        print(error.validator)
        print(error.obj)
        print(error.decoder)
        print(error.reason)
        print(error.source)
        print(error.namespaces)
        stopTime = datetime.datetime.now()

    ts = stopTime - startTime
    print('zwalidowano w czasie: ', ts.seconds)




    # mh = MessageHandler()
    #
    # schemaUrl = QUrl.fromLocalFile(xsdPath)
    # schema = QXmlSchema()
    # schema.load(schemaUrl)
    # print('schema')
    # if schema.isValid():
    #     file = QFile(xmlPath)
    #     file.open(QIODevice.ReadOnly)
    #     validator = QXmlSchemaValidator(schema)
    #     validator.setMessageHandler(mh)
    #     result = validator.validate(file, QUrl.fromLocalFile(file.fileName()))
    #
    #     if result:
    #         print("valid")
    #     else:
    #         print("invalid")
    #         print(mh.getMessageType())
    #         print(mh.getDescription())
    #         print(mh.getSourceLocation())
    # else:
    #     print('schema invalid')

