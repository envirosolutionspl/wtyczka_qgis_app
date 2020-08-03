import xml.etree.ElementTree as ET


def xmlToMetadataElementDict(xml):
    """słownik metadataElementDict na podstawie pliku XML"""
    metadataElementDict = {}

    ns = {'gco': "http://www.isotc211.org/2005/gco",
          'gmx': "http://www.isotc211.org/2005/gmx",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gml': "http://www.opengis.net/gml",
          'srv': "http://www.isotc211.org/2005/srv",
          'xs': "http://www.w3.org/2001/XMLSchema",
          'xsi': "http://www.w3.org/2001/XMLSchema-instance"
          }
    root = ET.parse(xml)

    # E1
    element = root.find('//*/gmd:MD_DataIdentification/*/gmd:CI_Citation/gmd:title/gco:CharacterString', ns)
    if element is not None:
        data = {'e1_lineEdit': element.text}
        metadataElementDict['e1'] = data

    # E2
    element = root.find('//*/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString', ns)
    if element is not None:
        data = {'e2_lineEdit': element.text}
        metadataElementDict['e2'] = data

    return metadataElementDict