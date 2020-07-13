class FormElement:

    def __init__(self, name, form, type='', minOccurs=1, documentation=''):
        self.setName(name)
        self.setType(type)
        self.setMinOccurs(minOccurs)
        self.setDocumentation(documentation)
        self.__isComplex = False
        self.innerFormElements = []
        self.isNillable = False
        self.form = form    # wskazanie formularza do ktorego obiekt nalezy

    def setName(self, name):
        self.name = name

    def setType(self, type):
        self.type = type

    def setNillable(self):
        self.isNillable = True

    def setMinOccurs(self, minOccurs):
        self.minOccurs = int(minOccurs)

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