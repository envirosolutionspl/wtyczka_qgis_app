from PyQt5.QtWidgets import QWidget, QListWidget, QLineEdit, QCheckBox, QComboBox, QDateTimeEdit, QListWidgetItem
from PyQt5.QtCore import Qt, QVariant
from .. import utils
def metadataElementDictToForm(metadataElementDict, targetForm):
    """aktualizuje formularz na podstawie słownika metadataElementDict"""

    for elementId, formDefinition in metadataElementDict.items():
        if type(formDefinition) is list:    # element wielokrotny (listWidget)
            listWidget = utils.getWidgetByName(layout=targetForm, searchObjectType=QListWidget, name=elementId + '_listWidget')
            listWidget.clear()
            for data in formDefinition:
                item = QListWidgetItem()
                item.setData(Qt.UserRole, QVariant(data))
                item.setText(list(data.values())[0])
                listWidget.addItem(item)

        else:   # pojedyncze elementy np. lineEdit
            for inputName, value in formDefinition.items():
                input = utils.getWidgetByName(layout=targetForm, searchObjectType=QWidget, name=inputName)
                if isinstance(input, QComboBox):
                    input.setCurrentIndex(input.findText(value))
                elif isinstance(input, QDateTimeEdit):
                    input.setDateTime(value)
                elif isinstance(input, QLineEdit):
                    input.setText(value)
