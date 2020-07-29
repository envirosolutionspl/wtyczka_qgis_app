import xml.etree.ElementTree as ET

def appGmlToMetadataElementDict(gmlPath):
    """słownik metadataElementDict na podstawie pliku zbioru APP"""
    metadataElementDict = {}

    ns = {'gco': "http://www.isotc211.org/2005/gco",
          'app': "http://zagospodarowanieprzestrzenne.gov.pl/schemas/app/1.0",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gml': "http://www.opengis.net/gml/3.2",
          'wfs': "http://www.opengis.net/wfs/2.0",
          'xlink': "http://www.w3.org/1999/xlink",
          'xsi': "http://www.w3.org/2001/XMLSchema-instance"
          }

    root = ET.parse(gmlPath)

    # E16
    itemsList = []
    for rozdzielczosc in root.findall('//*/app:rozdzielczoscPrzestrzenna', ns):
        if rozdzielczosc.text not in itemsList:
            itemsList.append({'e16_lineEdit': rozdzielczosc.text})
            print(rozdzielczosc.text)
    metadataElementDict['e16'] = itemsList

    return metadataElementDict