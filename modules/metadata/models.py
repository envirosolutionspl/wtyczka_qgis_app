class MetadataElement:
    """podejynczy element metadanych według katalogu metadanych"""

    def __init__(self, elementId, licznosc):
        self.elementId = elementId
        self.licznosc = licznosc
        self.widgets = []

    def setWidgets(self, widgets):
        self.widgets = widgets

    def getWidgets(self):
        return self.widgets