class FormElement:
    def __init__(self, name, type='', minOccurs=-1, documentation=''):
        self.setName(name)
        self.setType(type)
        self.setMinOccurs(minOccurs)
        self.setDocumentation(documentation)

    def setName(self, name):
        self.name = name

    def setType(self, type):
        self.type = type

    def setMinOccurs(self, minOccurs):
        self.minOccurs = minOccurs

    def setDocumentation(self, documentation):
        self.documentation = documentation