class FormElement:
    """ reprezentuje element definicji formularza zdefiniowany w XSD"""
    def __init__(self, name, form, type='', minOccurs=1, documentation=''):
        self.setName(name)
        self.setType(type)
        self.setMinOccurs(minOccurs)
        self.setDocumentation(documentation)
        self.__isComplex = False
        self.innerFormElements = []
        self.isNillable = False
        self.maxOccurs = None
        self.form = form    # wskazanie formularza do ktorego obiekt nalezy

    def setName(self, name):
        self.name = name

    def setType(self, type):
        self.type = type

    def setNillable(self):
        self.isNillable = True

    def setMinOccurs(self, minOccurs):
        self.minOccurs = int(minOccurs)

    def setMaxOccurs(self, maxOccurs):
        self.maxOccurs = maxOccurs

    def setDocumentation(self, documentation):
        self.documentation = documentation

    def markAsComplex(self):
        self.__isComplex = True

    def isComplex(self):
        return self.__isComplex

    def setInnerFormElement(self, form):
        if self.isComplex():
            self.innerFormElements.append(form)
        else:
            raise NotImplementedError


class AppTableModel:
    """Wiersz tabeli przygotowanai zbioru APP"""
    def __init__(self, rowId, path, date):
        self.rowId = rowId
        self.path = path
        self.date = date

    def __str__(self):
        return "%s, %s, %s" % (self.rowId, self.path, self.date)
