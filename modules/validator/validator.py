# -*- coding: utf-8 -*-
import lxml
import os
import datetime
import xml.etree.ElementTree as ET
from . import validator_utils
from qgis.core import QgsVectorLayer
from ..app.app_utils import isLayerInPoland
from ..metadata.metadata_import_export import xmlToMetadataElementDict, xmlToMetadataElementDictFixed
from .. import dictionaries, utils
import processing
xsdPath = os.path.join(os.path.dirname(__file__), 'planowaniePrzestrzenne.xsd')


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
                errors.append("Błąd w linii %s: %s" % (
                    error.line, error.message.encode("utf-8").decode("utf-8")))

            return [False, '\n\n'.join(errors)]

    def validateMetadataXml(self, xmlPath):
        valResult = self.validateXml(xmlPath)
        if valResult[0]:
            valTagsResult = self.validateRequiredMetadataTags(xmlPath)
            if not valTagsResult[0]:
                return valTagsResult
        return valResult

    def validateAppXml(self, xmlPath):
        print('walidator')
        valResult = self.validateXml(xmlPath)
        if valResult[0]:
            layer = QgsVectorLayer(xmlPath + '|layername=AktPlanowaniaPrzestrzennego', "gml", 'ogr')
            # if not layer.isValid():
            #     layer = QgsVectorLayer(xmlPath + '|layername=featureMember', "gml", 'ogr')
            if layer and layer.isValid():
                if not isLayerInPoland(layer):
                    return [False,
                            'Błąd geometrii APP: Obrysy leżą poza granicami Polski. Sprawdź czy w pliku GML jest prawidłowa definicja układu zgodnie ze standardem INSPIRE np: srsName="http://www.opengis.net/def/crs/EPSG/0/2177"']
            else:
                return [False, 'Błąd geometrii APP: Geometria APP nie jest poprawną warstwą wektorową lub brak poprawnie zdefiniowanego elementu \"AktPlanowaniaPrzestrzennego\" w GML']

            # walidacja unikalności przestrzeni nazw w pliku GML
            valRelationsResult = self.validatePrzestrzenNazwIntegrity(xmlPath)
            if not valRelationsResult[0]:
                return valRelationsResult

            # walidacja obligatoryjności mapy podkładowej tylko dla APP poziomu lokalnego
            valRelationsResult = self.validateMapaPodkladowaQuantityRequirement(xmlPath)
            if not valRelationsResult[0]:
                return valRelationsResult

            # walidacja relacji
            valRelationsResult = self.validateAppRelations(xmlPath)
            if not valRelationsResult[0]:
                return valRelationsResult

        return valResult

    def validateZbiorXml(self, xmlPath):

        # walidacja założeń APP
        valRes = self.validateAppXml(xmlPath)
        if not valRes[0]:
            return valRes

        # walidacja nakładania się aktualnych zbiorów
        valOverlayResult = utils.checkZbiorGeometryValidityOnCreatedFile(xmlPath)
        if not valOverlayResult[0]:
            return valOverlayResult

        return [True]


    def validateRequiredMetadataTags(self, xmlPath):
        """sprawdza czy są wszystkie wymagane tagi w metadanych"""
        bledy = []
        metadataElementDict = xmlToMetadataElementDict(xmlPath)

        for elementId, content in metadataElementDict.items():
            licznosc = dictionaries.licznoscMetadataFields[elementId]
            # element wymagany i nie ma go w XML
            if int(licznosc[0]) > 0 and not content:
                bledy.append('Brak definicji wymaganej wartości \'%s\' (%s) z katalogu metadanych w walidowanym pliku XML metadanych' % (
                        dictionaries.nazwyMetadataFields[elementId], elementId))
        if bledy:
            return [False, '\n\n'.join(bledy)]
        return [True]

    def validateAppRelations(self, gmlPath):
        """Sprawdza czy relacje wewnątrz zbioru są zgodne"""
        ns = {'gco': "http://www.isotc211.org/2005/gco",
              'app': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/1.0",
              'gmd': "http://www.isotc211.org/2005/gmd",
              'gml': "http://www.opengis.net/gml/3.2",
              'wfs': "http://www.opengis.net/wfs/2.0",
              'xlink': "http://www.w3.org/1999/xlink",
              'xsi': "http://www.w3.org/2001/XMLSchema-instance"
              }

        root = ET.parse(gmlPath)

        # przystąpienie
        bledy = []
        for app in root.findall('//app:AktPlanowaniaPrzestrzennego', ns):

            # przystapienie
            dok_przystepujacy = app.find('./app:dokumentPrzystepujacy', ns)
            if dok_przystepujacy is not None:
                dok_przystepujacy_id = dok_przystepujacy.attrib['{%s}href' %
                                                                ns['xlink']]
                df = root.find('//app:DokumentFormalny[@{%s}id="%s"]' % (
                    ns['gml'], validator_utils.urlIdToGmlId(dok_przystepujacy_id)), ns)
                if df is None:
                    bledy.append('Brak dokumentu formalnego o identyfikatorze %s' %
                                 validator_utils.urlIdToGmlId(dok_przystepujacy_id))
                else:
                    przystapienie = df.find('./app:przystapienie', ns)
                    if przystapienie is None:
                        bledy.append('Brak zdefiniowanej relacji \'przystapienie\' dla dokumentu formalnego o identyfikatorze %s' %
                                     validator_utils.urlIdToGmlId(dok_przystepujacy_id))

            # uchwala
            dok_uchwalajacy = app.find('./app:dokumentUchwalajacy', ns)
            if dok_uchwalajacy is not None:
                dok_uchwalajacy_id = dok_uchwalajacy.attrib['{%s}href' %
                                                            ns['xlink']]
                df = root.find('//app:DokumentFormalny[@{%s}id="%s"]' % (
                    ns['gml'], validator_utils.urlIdToGmlId(dok_uchwalajacy_id)), ns)
                if df is None:
                    bledy.append('Brak dokumentu formalnego o identyfikatorze %s' %
                                 validator_utils.urlIdToGmlId(dok_uchwalajacy_id))
                else:
                    uchwala = df.find('./app:uchwala', ns)
                    if uchwala is None:
                        bledy.append(
                            'Brak zdefiniowanej relacji \'uchwala\' dla dokumentu formalnego o identyfikatorze %s' % validator_utils.urlIdToGmlId(dok_uchwalajacy_id))

            # zmienia
            dok_zmieniajacy = app.find('./app:dokumentZmieniajacy', ns)
            if dok_zmieniajacy is not None:
                dok_zmieniajacy_id = dok_zmieniajacy.attrib['{%s}href' %
                                                            ns['xlink']]
                df = root.find('//app:DokumentFormalny[@{%s}id="%s"]' % (
                    ns['gml'], validator_utils.urlIdToGmlId(dok_zmieniajacy_id)), ns)
                if df is None:
                    bledy.append('Brak dokumentu formalnego o identyfikatorze %s' %
                                 validator_utils.urlIdToGmlId(dok_zmieniajacy_id))
                else:
                    zmienia = df.find('./app:zmienia', ns)
                    if zmienia is None:
                        bledy.append(
                            'Brak zdefiniowanej relacji \'zmienia\' dla dokumentu formalnego o identyfikatorze %s' % validator_utils.urlIdToGmlId(dok_zmieniajacy_id))

            # uchyla
            dok_uchylajacy = app.find('./app:dokumentUchylajacy', ns)
            if dok_uchylajacy is not None:
                dok_uchylajacy_id = dok_uchylajacy.attrib['{%s}href' %
                                                          ns['xlink']]
                df = root.find('//app:DokumentFormalny[@{%s}id="%s"]' % (
                    ns['gml'], validator_utils.urlIdToGmlId(dok_uchylajacy_id)), ns)
                if df is None:
                    bledy.append('Brak dokumentu formalnego o identyfikatorze %s' %
                                 validator_utils.urlIdToGmlId(dok_uchylajacy_id))
                else:
                    uchyla = df.find('./app:zmienia', ns)
                    if uchyla is None:
                        bledy.append(
                            'Brak zdefiniowanej relacji \'uchyla\' dla dokumentu formalnego o identyfikatorze %s' % validator_utils.urlIdToGmlId(dok_uchylajacy_id))

            # uniewaznia
            dok_uniewazniajacy = app.find('./app:dokumentUniewazniajacy', ns)
            if dok_uniewazniajacy is not None:
                dok_uniewazniajacy_id = dok_uniewazniajacy.attrib['{%s}href' %
                                                                  ns['xlink']]
                df = root.find('//app:DokumentFormalny[@{%s}id="%s"]' % (
                    ns['gml'], validator_utils.urlIdToGmlId(dok_uniewazniajacy_id)), ns)
                if df is None:
                    bledy.append('Brak dokumentu formalnego o identyfikatorze %s' %
                                 validator_utils.urlIdToGmlId(dok_uniewazniajacy_id))
                else:
                    uniewaznia = df.find('./app:zmienia', ns)
                    if uniewaznia is None:
                        bledy.append('Brak zdefiniowanej relacji \'uniewaznia\' dla dokumentu formalnego o identyfikatorze %s' %
                                     validator_utils.urlIdToGmlId(dok_uniewazniajacy_id))

        if bledy:
            return False, '\n\n'.join(bledy)

        return [True]

    def validatePrzestrzenNazwIntegrity(self, gmlPath):
        """Sprawdza czy przestrzenie nazw są zgodne"""
        ns = {'gco': "http://www.isotc211.org/2005/gco",
              'app': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/1.0",
              'gmd': "http://www.isotc211.org/2005/gmd",
              'gml': "http://www.opengis.net/gml/3.2",
              'wfs': "http://www.opengis.net/wfs/2.0",
              'xlink': "http://www.w3.org/1999/xlink",
              'xsi': "http://www.w3.org/2001/XMLSchema-instance"
              }

        root = ET.parse(gmlPath)

        przestrzenie = []
        # wydobycie unikalnych przestrzeni nazw
        for p in root.findall('//app:idIIP/app:Identyfikator/app:przestrzenNazw', ns):
            przestrzenie.append(p.text)
        unikalnePrzestrzenie = list(set(przestrzenie))

        if len(unikalnePrzestrzenie) == 0:
            return False, 'Brak zdefiniowanych przestrzeni nazw w pliku'
        elif len(unikalnePrzestrzenie) > 1:
            return False, 'W APP/Zbiorze APP może występować TYLKO JEDNA przestrzeń nazw. \nW pliku %s znajdują się następujące przestrzenie nazw:\n\n%s' % (
                gmlPath,
                '\n'.join(unikalnePrzestrzenie)
            )
        else:
            return [True]

    def validateMapaPodkladowaQuantityRequirement(self, gmlPath):
        """Sprawdza czy przestrzenie nazw są zgodne"""
        ns = {'gco': "http://www.isotc211.org/2005/gco",
              'app': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/1.0",
              'gmd': "http://www.isotc211.org/2005/gmd",
              'gml': "http://www.opengis.net/gml/3.2",
              'wfs': "http://www.opengis.net/wfs/2.0",
              'xlink': "http://www.w3.org/1999/xlink",
              'xsi': "http://www.w3.org/2001/XMLSchema-instance"
              }

        root = ET.parse(gmlPath)

        bledy = []
        # wydobycie unikalnych przestrzeni nazw
        for app in root.findall('//app:AktPlanowaniaPrzestrzennego', ns):
            poziomHierarchii = app.find('app:poziomHierarchii', ns)
            poziom = poziomHierarchii.attrib['{%s}title' % ns['xlink']]
            print(poziom)
            if poziom == 'lokalny':
                mapyPodkladowe = app.findall('app:mapaPodkladowa/app:MapaPodkladowa/app:referencja', ns)
                print(len(mapyPodkladowe))
                if len(mapyPodkladowe) == 0:
                    appId = validator_utils.urlIdToGmlId(app.find('gml:identifier', ns).text)
                    bledy.append(
                        f'Dla Aktu Planowania Przestrzennego o identyfikatorze {appId} brak definicji atrybutu \'mapaPodkladowa\'.\nAtrybut \'mapaPodkladowa\' jest wymagany dla wszystkich APP poziomu lokalnego (poziomHierarchii = http://inspire.ec.europa.eu/codelist/LevelOfSpatialPlanValue/local)')

        if len(bledy) > 0:
            return False, '\n'.join(bledy)
        else:
            return [True]
