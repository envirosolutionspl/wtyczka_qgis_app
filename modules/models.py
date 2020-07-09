class FormElement:
    def __init__(self, name, type='', minOccurs=1, documentation=''):
        self.setName(name)
        self.setType(type)
        self.setMinOccurs(minOccurs)
        self.setDocumentation(documentation)
        self.isComplex = False
        self.innerFormElements = []

    def setName(self, name):
        self.name = name

    def setType(self, type):
        self.type = type

    def setMinOccurs(self, minOccurs):
        self.minOccurs = int(minOccurs)

    def setDocumentation(self, documentation):
        self.documentation = documentation

    def markAsComplex(self):
        self.isComplex = True

    def setInnerFormElement(self, form):
        if self.isComplex:
            self.innerFormElements.append(form)
        else:
            raise NotImplementedError