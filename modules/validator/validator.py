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
            # walidacja relacji
            valRelationsResult = self.validateZbiorRelations(xmlPath)
            if not valRelationsResult[0]:
                return valRelationsResult
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

    def validateZbiorRelations(self, gmlPath):
        """Sprawdza czy relacje wewnątrz zbioru są zgodne"""
        ns = {'gco': "http://www.isotc211.org/2005/gco",
              'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
              'gmd': "http://www.isotc211.org/2005/gmd",
              'gml': "http://www.opengis.net/gml/3.2",
              'wfs': "http://www.opengis.net/wfs/2.0",
              'xlink': "http://www.w3.org/1999/xlink",
              'xsi': "http://www.w3.org/2001/XMLSchema-instance"
              }

        root = ET.parse(gmlPath)

        # przystąpienie
        bledy = []
        for app in root.findall('/wfs:member/app:AktPlanowaniaPrzestrzennego', ns):
            # identifier = app.find('./gml:identifier', ns).text

            # przystapienie
            dok_przystepujacy = app.find('./app:dokumentPrzystepujacy', ns)
            if dok_przystepujacy is not None:
                dok_przystepujacy_id = dok_przystepujacy.attrib['{%s}href' % ns['xlink']]
                df = root.find('/wfs:member/app:DokumentFormalny[@{%s}id="%s"]' % (ns['gml'], dok_przystepujacy_id.split('/')[-1]), ns)
                if df is None:
                    bledy.append('Brak dokumentu formalnego o identyfikatorze %s' % dok_przystepujacy_id.split('/')[-1])
                else:
                    przystapienie = df.find('./app:przystapienie', ns)
                    if przystapienie is None:
                        bledy.append('Brak zdefiniowanej relacji \'przystapienie\' dla dokumentu formalnego o identyfikatorze %s' % dok_przystepujacy_id.split('/')[-1])

            # uchwala
            dok_uchwalajacy = app.find('./app:dokumentUchwalajacy', ns)
            if dok_uchwalajacy is not None:
                dok_uchwalajacy_id = dok_uchwalajacy.attrib['{%s}href' % ns['xlink']]
                df = root.find('/wfs:member/app:DokumentFormalny[@{%s}id="%s"]' % (ns['gml'], dok_uchwalajacy_id.split('/')[-1]), ns)
                if df is None:
                    bledy.append('Brak dokumentu formalnego o identyfikatorze %s' % dok_uchwalajacy_id.split('/')[-1])
                else:
                    uchwala = df.find('./app:uchwala', ns)
                    if uchwala is None:
                        bledy.append('Brak zdefiniowanej relacji \'uchwala\' dla dokumentu formalnego o identyfikatorze %s' % dok_uchwalajacy_id.split('/')[-1])

            # zmienia
            dok_zmieniajacy = app.find('./app:dokumentZmieniajacy', ns)
            if dok_zmieniajacy is not None:
                dok_zmieniajacy_id = dok_zmieniajacy.attrib['{%s}href' % ns['xlink']]
                df = root.find('/wfs:member/app:DokumentFormalny[@{%s}id="%s"]' % (ns['gml'], dok_zmieniajacy_id.split('/')[-1]), ns)
                if df is None:
                    bledy.append('Brak dokumentu formalnego o identyfikatorze %s' % dok_zmieniajacy_id.split('/')[-1])
                else:
                    zmienia = df.find('./app:zmienia', ns)
                    if zmienia is None:
                        bledy.append('Brak zdefiniowanej relacji \'zmienia\' dla dokumentu formalnego o identyfikatorze %s' % dok_zmieniajacy_id.split('/')[-1])

            # uchyla
            dok_uchylajacy = app.find('./app:dokumentUchylajacy', ns)
            if dok_uchylajacy is not None:
                dok_uchylajacy_id = dok_uchylajacy.attrib['{%s}href' % ns['xlink']]
                df = root.find('/wfs:member/app:DokumentFormalny[@{%s}id="%s"]' % (ns['gml'], dok_uchylajacy_id.split('/')[-1]), ns)
                if df is None:
                    bledy.append('Brak dokumentu formalnego o identyfikatorze %s' % dok_uchylajacy_id.split('/')[-1])
                else:
                    uchyla = df.find('./app:zmienia', ns)
                    if uchyla is None:
                        bledy.append('Brak zdefiniowanej relacji \'uchyla\' dla dokumentu formalnego o identyfikatorze %s' % dok_uchylajacy_id.split('/')[-1])

            # uniewaznia
            dok_uniewazniajacy = app.find('./app:dokumentUniewazniajacy', ns)
            if dok_uniewazniajacy is not None:
                dok_uniewazniajacy_id = dok_uniewazniajacy.attrib['{%s}href' % ns['xlink']]
                df = root.find('/wfs:member/app:DokumentFormalny[@{%s}id="%s"]' % (ns['gml'], dok_uniewazniajacy_id.split('/')[-1]), ns)
                if df is None:
                    bledy.append('Brak dokumentu formalnego o identyfikatorze %s' % dok_uniewazniajacy_id.split('/')[-1])
                else:
                    uniewaznia = df.find('./app:zmienia', ns)
                    if uniewaznia is None:
                        bledy.append('Brak zdefiniowanej relacji \'uniewaznia\' dla dokumentu formalnego o identyfikatorze %s' % dok_uniewazniajacy_id.split('/')[-1])

        if bledy:
            return False, '\n\n'.join(bledy)

        return [True]
