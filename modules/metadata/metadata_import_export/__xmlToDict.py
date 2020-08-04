import xml.etree.ElementTree as ET
from PyQt5.QtCore import QDateTime
from . import translation
from .. import utils

def xmlToMetadataElementDict(xml):
    """słownik metadataElementDict na podstawie pliku XML"""
    metadataElementDict = {}

    ns = {'gco': "http://www.isotc211.org/2005/gco",
          'gmx': "http://www.isotc211.org/2005/gmx",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gml': "http://www.opengis.net/gml",
          'srv': "http://www.isotc211.org/2005/srv",
          'xlink': "http://www.w3.org/1999/xlink",
          'xs': "http://www.w3.org/2001/XMLSchema",
          'xsi': "http://www.w3.org/2001/XMLSchema-instance"
          }
    root = ET.parse(xml)

    # E1
    element = root.find('//gmd:MD_DataIdentification/*/gmd:CI_Citation/gmd:title/gco:CharacterString', ns)
    if element is not None:
        data = {'e1_lineEdit': element.text}
        metadataElementDict['e1'] = data

    # E2
    element = root.find('//gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString', ns)
    if element is not None:
        data = {'e2_lineEdit': element.text}
        metadataElementDict['e2'] = data

    # E4
    itemsList = []
    for element in root.findall('//gmd:transferOptions//gmd:linkage/gmd:URL', ns):
        if element.text not in itemsList:
            itemsList.append({'e4_lineEdit': element.text})
    metadataElementDict['e4'] = itemsList

    # E5
    itemsList = []
    for element in root.findall('//gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier//gco:CharacterString', ns):
        if element.text not in itemsList:
            itemsList.append({'e5_lineEdit': element.text})
    metadataElementDict['e5'] = itemsList

    # E6
    itemsList = []
    for element in root.findall(
            '//gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode', ns):
        if element.text not in itemsList:
            itemsList.append({'e6_lineEdit': element.text})
    metadataElementDict['e6'] = itemsList

    # E7
    itemsList = []
    for element in root.findall(
            '/gmd:characterSet/gmd:MD_CharacterSetCode', ns):
        if element.attrib['codeListValue'] not in itemsList:
            itemsList.append({'e7_cmbbx': element.attrib['codeListValue']})
    metadataElementDict['e7'] = itemsList

    # E9 E10
    itemsList = []
    for descriptiveKeywords in root.findall(
            '//gmd:MD_DataIdentification/gmd:descriptiveKeywords', ns):
        data = {}

        keyword = descriptiveKeywords.find('.//gmd:keyword/gmx:Anchor', ns) # złożony KeyWord
        keywordSimple = descriptiveKeywords.find('.//gmd:keyword/gco:CharacterString', ns)   # prosty KeyWord
        if keyword is not None and keyword.text not in data:
            data['e9_lineEdit'] = keyword.text
        elif keywordSimple is not None and keywordSimple.text not in data:
            data['e9_lineEdit'] = keywordSimple.text

        thesaurus = descriptiveKeywords.find('.//gmd:thesaurusName', ns)
        if thesaurus is not None:
            thesaurus_title = thesaurus.find('.//gmd:title/gmx:Anchor', ns)
            data['e10_lineEdit'] = thesaurus_title.text
            data['xlink'] = thesaurus_title.attrib['{%s}href' % ns['xlink']]
            date = thesaurus.find('.//gco:Date', ns)
            data['e10_dateTimeEdit'] = QDateTime.fromString(date.text, "yyyy-MM-dd")
            dateTypeCode = thesaurus.find('.//gmd:CI_DateTypeCode', ns)
            data['e10_cmbbx'] = utils.getKeyByValue(translation, dateTypeCode.attrib['codeListValue'])


        itemsList.append(data)
    metadataElementDict['e9'] = itemsList


    return metadataElementDict