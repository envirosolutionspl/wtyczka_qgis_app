from qgis.core import QgsSettings
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def initializeMetadataForm(dlg):
    s = QgsSettings()

    name = s.value("qgis_app/settings/contactName", "")
    mail = s.value("qgis_app/settings/contactMail", "")
    if name and mail:
        data = {
            'e22_name_lineEdit': name,
            'e22_mail_lineEdit': mail,
            'e23_cmbbx': 'punkt kontaktowy'
        }
        item = QListWidgetItem()
        item.setData(Qt.UserRole, QVariant(data))
        item.setText("%s - %s - %s" % (name, mail, 'punkt kontaktowy'))
        dlg.e22_listWidget.addItem(item)
        data = {
            'e29_name_lineEdit': name,
            'e29_mail_lineEdit': mail,
            'e29_cmbbx': 'punkt kontaktowy'
        }
        item = QListWidgetItem()
        item.setData(Qt.UserRole, QVariant(data))
        item.setText("%s - %s - %s" % (name, mail, 'punkt kontaktowy'))
        dlg.e29_listWidget.addItem(item)