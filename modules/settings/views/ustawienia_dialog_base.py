# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ustawienia_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(487, 508)
        self.gridLayout_3 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_lbl = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title_lbl.setFont(font)
        self.title_lbl.setObjectName("title_lbl")
        self.verticalLayout.addWidget(self.title_lbl)
        self.empty_lbl = QtWidgets.QLabel(Dialog)
        self.empty_lbl.setText("")
        self.empty_lbl.setObjectName("empty_lbl")
        self.verticalLayout.addWidget(self.empty_lbl)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.settings_scrollArea = QtWidgets.QScrollArea(Dialog)
        self.settings_scrollArea.setWidgetResizable(True)
        self.settings_scrollArea.setObjectName("settings_scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 438, 428))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalGroupBox = QgsCollapsibleGroupBox(self.scrollAreaWidgetContents_2)
        self.verticalGroupBox.setObjectName("verticalGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.folder_btn = QtWidgets.QPushButton(self.verticalGroupBox)
        self.folder_btn.setObjectName("folder_btn")
        self.verticalLayout_4.addWidget(self.folder_btn)
        self.folder_lbl = QtWidgets.QLabel(self.verticalGroupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.folder_lbl.setFont(font)
        self.folder_lbl.setText("")
        self.folder_lbl.setObjectName("folder_lbl")
        self.verticalLayout_4.addWidget(self.folder_lbl)
        self.verticalLayout_2.addWidget(self.verticalGroupBox)
        self.verticalGroupBox_2 = QgsCollapsibleGroupBox(self.scrollAreaWidgetContents_2)
        self.verticalGroupBox_2.setObjectName("verticalGroupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalGroupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.przestrzenNazw_lineEdit = QgsFilterLineEdit(self.verticalGroupBox_2)
        self.przestrzenNazw_lineEdit.setProperty("qgisRelation", "")
        self.przestrzenNazw_lineEdit.setObjectName("przestrzenNazw_lineEdit")
        self.gridLayout_4.addWidget(self.przestrzenNazw_lineEdit, 0, 1, 1, 1)
        self.przestrzenNazw_lbl = QtWidgets.QLabel(self.verticalGroupBox_2)
        self.przestrzenNazw_lbl.setObjectName("przestrzenNazw_lbl")
        self.gridLayout_4.addWidget(self.przestrzenNazw_lbl, 0, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_4)
        self.verticalLayout_2.addWidget(self.verticalGroupBox_2)
        self.verticalGroupBox1 = QgsCollapsibleGroupBox(self.scrollAreaWidgetContents_2)
        self.verticalGroupBox1.setObjectName("verticalGroupBox1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalGroupBox1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.contactMail_lineEdit = QgsFilterLineEdit(self.verticalGroupBox1)
        self.contactMail_lineEdit.setProperty("qgisRelation", "")
        self.contactMail_lineEdit.setObjectName("contactMail_lineEdit")
        self.gridLayout_2.addWidget(self.contactMail_lineEdit, 1, 1, 1, 1)
        self.contactMail_lbl = QtWidgets.QLabel(self.verticalGroupBox1)
        self.contactMail_lbl.setObjectName("contactMail_lbl")
        self.gridLayout_2.addWidget(self.contactMail_lbl, 1, 0, 1, 1)
        self.contactName_lbl = QtWidgets.QLabel(self.verticalGroupBox1)
        self.contactName_lbl.setObjectName("contactName_lbl")
        self.gridLayout_2.addWidget(self.contactName_lbl, 0, 0, 1, 1)
        self.contactName_lineEdit = QgsFilterLineEdit(self.verticalGroupBox1)
        self.contactName_lineEdit.setProperty("qgisRelation", "")
        self.contactName_lineEdit.setObjectName("contactName_lineEdit")
        self.gridLayout_2.addWidget(self.contactName_lineEdit, 0, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.verticalLayout_2.addWidget(self.verticalGroupBox1)
        self.verticalGroupBox2 = QgsCollapsibleGroupBox(self.scrollAreaWidgetContents_2)
        self.verticalGroupBox2.setObjectName("verticalGroupBox2")
        self.verticalLayout_31 = QtWidgets.QVBoxLayout(self.verticalGroupBox2)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.gridLayout_21 = QtWidgets.QGridLayout()
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.adminMail_lineEdit = QgsFilterLineEdit(self.verticalGroupBox2)
        self.adminMail_lineEdit.setProperty("qgisRelation", "")
        self.adminMail_lineEdit.setObjectName("adminMail_lineEdit")
        self.gridLayout_21.addWidget(self.adminMail_lineEdit, 1, 1, 1, 1)
        self.adminMail_lbl = QtWidgets.QLabel(self.verticalGroupBox2)
        self.adminMail_lbl.setObjectName("adminMail_lbl")
        self.gridLayout_21.addWidget(self.adminMail_lbl, 1, 0, 1, 1)
        self.adminName_lbl = QtWidgets.QLabel(self.verticalGroupBox2)
        self.adminName_lbl.setObjectName("adminName_lbl")
        self.gridLayout_21.addWidget(self.adminName_lbl, 0, 0, 1, 1)
        self.adminName_lineEdit = QgsFilterLineEdit(self.verticalGroupBox2)
        self.adminName_lineEdit.setProperty("qgisRelation", "")
        self.adminName_lineEdit.setObjectName("adminName_lineEdit")
        self.gridLayout_21.addWidget(self.adminName_lineEdit, 0, 1, 1, 1)
        self.verticalLayout_31.addLayout(self.gridLayout_21)
        self.verticalLayout_2.addWidget(self.verticalGroupBox2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.smtp_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.smtp_btn.setObjectName("smtp_btn")
        self.horizontalLayout_3.addWidget(self.smtp_btn)
        self.csw_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.csw_btn.setObjectName("csw_btn")
        self.horizontalLayout_3.addWidget(self.csw_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.settings_scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout.addWidget(self.settings_scrollArea)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.empty2_lbl = QtWidgets.QLabel(Dialog)
        self.empty2_lbl.setText("")
        self.empty2_lbl.setObjectName("empty2_lbl")
        self.verticalLayout.addWidget(self.empty2_lbl)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.save_btn = QtWidgets.QPushButton(Dialog)
        self.save_btn.setObjectName("save_btn")
        self.horizontalLayout_2.addWidget(self.save_btn)
        self.exit_btn = QtWidgets.QPushButton(Dialog)
        self.exit_btn.setEnabled(True)
        self.exit_btn.setObjectName("exit_btn")
        self.horizontalLayout_2.addWidget(self.exit_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_lbl.setText(_translate("Dialog", "Ustawienia wtyczki APP"))
        self.verticalGroupBox.setTitle(_translate("Dialog", "Domyślna ścieżka zapisu plików"))
        self.folder_btn.setText(_translate("Dialog", "Wybierz katalog"))
        self.verticalGroupBox_2.setTitle(_translate("Dialog", "Domyślne wartości atrybutów"))
        self.przestrzenNazw_lbl.setText(_translate("Dialog", "przestrzenNazw"))
        self.verticalGroupBox1.setTitle(_translate("Dialog", "Domyślny punkt kontaktowy"))
        self.contactMail_lbl.setText(_translate("Dialog", "Adres email"))
        self.contactName_lbl.setText(_translate("Dialog", "Nazwa       "))
        self.verticalGroupBox2.setTitle(_translate("Dialog", "Administrator danych"))
        self.adminMail_lbl.setText(_translate("Dialog", "Adres email"))
        self.adminName_lbl.setText(_translate("Dialog", "Nazwa       "))
        self.smtp_btn.setText(_translate("Dialog", "Ustawienia serwera SMTP"))
        self.csw_btn.setText(_translate("Dialog", "Ustawienia serwera CSW"))
        self.save_btn.setText(_translate("Dialog", "Zapisz"))
        self.exit_btn.setText(_translate("Dialog", "Zamknij"))
from qgscollapsiblegroupbox import QgsCollapsibleGroupBox
from qgsfilterlineedit import QgsFilterLineEdit


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
