# -*- coding: utf-8 -*-
import os, datetime
import xml.etree.ElementTree as ET
from qgis.core import QgsVectorLayer
from ..app.app_utils import isLayerInPoland
from ..metadata.metadata_import_export import xmlToMetadataElementDict, xmlToMetadataElementDictFixed
from .. import dictionaries
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
        try:
            xml_root = lxml.etree.parse(xmlPath)
        except lxml.etree.XMLSyntaxError as e:  # błąd w składni XML
            return [False, "Błąd w składni XML:\n" + str(e.msg)]
        except OSError as e:  # błąd odczytu pliku
            return [False, "Błąd odczytu pliku lub plik nie istnieje:\n" + str(e.msg)]

        if self.schema.validate(xml_root):
            return [True]
        else:
            errors = []
            for error in self.schema.error_log:
                errors.append("Błąd w linii %s: %s" % (error.line, error.message.encode("utf-8").decode("utf-8")))

            return [False, '\n\n'.join(errors)]

    def validateMetadataXml(self, xmlPath):
        valResult = self.validateXml(xmlPath)
        if valResult[0]:
            valTagsResult = self.validateRequiredMetadataTags(xmlPath)
            if not valTagsResult[0]:
                return valTagsResult
        return valResult

    def validateZbiorXml(self, xmlPath):
        valResult = self.validateXml(xmlPath)
        if valResult[0]:
            layer = QgsVectorLayer(xmlPath + '|layername=AktPlanowaniaPrzestrzennego', "gml", 'ogr')
            if layer and layer.isValid():
                if not isLayerInPoland(layer):
                    return [False, 'Błąd geometrii zbioru: Obrysy leżą poza granicami Polski']
        return valResult

    def validateAppXml(self, xmlPath):
        valResult = self.validateXml(xmlPath)
        if valResult[0]:
            layer = QgsVectorLayer(xmlPath + '|layername=AktPlanowaniaPrzestrzennego', "gml", 'ogr')
            if layer and layer.isValid():
                if not isLayerInPoland(layer):
                    return [False, 'Błąd geometrii zbioru: Obrysy leżą poza granicami Polski']
        return valResult

    def validateRequiredMetadataTags(self, xmlPath):
        """sprawdza czy są wszystkie wymagane tagi w metadanych"""
        bledy = []
        metadataElementDict = xmlToMetadataElementDict(xmlPath)

        fixedElementsDict = xmlToMetadataElementDictFixed(xmlPath)
        unionDict = {**metadataElementDict, **fixedElementsDict}
        for elementId, licznosc in dictionaries.licznoscMetadataFields.items():
            if int(licznosc[0]) > 0 and elementId not in list(unionDict.keys()):  # element wymagany i nie ma go w XML
                bledy.append('Brak definicji wymaganej wartości \'%s\' (%s) z katalogu metadanych w walidowanym pliku XML metadanych' % (dictionaries.nazwyMetadataFields[elementId], elementId))
        if bledy:
            return [False, '\n\n'.join(bledy)]
        return [True]

