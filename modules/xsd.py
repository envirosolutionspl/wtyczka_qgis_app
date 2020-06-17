import os
from . import xmlschema
from .xmlschema.validators.exceptions import XMLSchemaDecodeError

# xsdPath = os.path.join(os.path.dirname(__file__), 'planowaniePrzestrzenne.xsd')
xsdPath = os.path.join(os.path.dirname(__file__), 'KlienciOrders.xsd')
xmlPath = os.path.join(os.path.dirname(__file__), 'invKlienciOrders.xml')


def validateXml(xmlPath=xmlPath, xsdPath=xsdPath):
    try:
        xmlschema.validate(xmlPath, xsdPath)
    except XMLSchemaDecodeError as error:
        print("błąd:\n")
        print(error.validator)
        print(error.obj)
        print(error.decoder)
        print(error.reason)
        print(error.source)
        print(error.namespaces)


