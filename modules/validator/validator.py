# -*- coding: utf-8 -*-
import os, datetime

xsdPath = os.path.join(os.path.dirname(__file__), 'planowaniePrzestrzenne.xsd')

import lxml

class ValidatorLxml:
    """Walidator oparty o bibliotekę lxml - wczytuje XSD z internetu 30-40 sekund """
    def __init__(self, schema_path=xsdPath):
        start = datetime.datetime.now()
        xsd_root = lxml.etree.parse(schema_path)
        self.schema = lxml.etree.XMLSchema(xsd_root)
        ts = datetime.datetime.now() - start
        print('wczytano XSD w: ', ts.seconds)

    def validateXml(self, xmlPath):
        print('validateXML')

        try:
            xml_root = lxml.etree.parse(xmlPath)
        except lxml.etree.XMLSyntaxError as e:  # błąd w składni XML
            return [False, "Błąd w składni XML:\n" + str(e.msg)]
        except OSError as e:  # błąd odczytu pliku
            return [False, "Błąd odczytu pliku:\n" + str(e.msg)]

        if self.schema.validate(xml_root):
            return [True]
        else:
            errors = []
            for error in self.schema.error_log:
                errors.append("Błąd w linii %s: %s" % (error.line, error.message.encode("utf-8").decode("utf-8")))

            return [False, '\n\n'.join(errors)]

    def validateMetadataXml(self, xmlPath):
        print('validate metadata')
        return self.validateXml(xmlPath)

    def validateZbiorXml(self, xmlPath):
        print('validate zbior')
        return self.validateXml(xmlPath)

    def validateAppXml(self, xmlPath):
        print('validate app')
        return self.validateXml(xmlPath)

