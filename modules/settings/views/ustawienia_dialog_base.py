# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ustawienia_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(500, 600)
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
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 482, 500))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.settings_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.settings_lbl.setWordWrap(True)
        self.settings_lbl.setObjectName("settings_lbl")
        self.gridLayout_2.addWidget(self.settings_lbl, 4, 1, 1, 1)
        self.settings_scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout.addWidget(self.settings_scrollArea)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.empty2_lbl = QtWidgets.QLabel(Dialog)
        self.empty2_lbl.setText("")
        self.empty2_lbl.setObjectName("empty2_lbl")
        self.verticalLayout.addWidget(self.empty2_lbl)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.save_btn = QtWidgets.QPushButton(Dialog)
        self.save_btn.setObjectName("save_btn")
        self.horizontalLayout_2.addWidget(self.save_btn)
        self.reset_btn = QtWidgets.QPushButton(Dialog)
        self.reset_btn.setObjectName("reset_btn")
        self.horizontalLayout_2.addWidget(self.reset_btn)
        self.cancel_btn = QtWidgets.QPushButton(Dialog)
        self.cancel_btn.setEnabled(True)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_2.addWidget(self.cancel_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_lbl.setText(_translate("Dialog", "Ustawienia wtyczki APP"))
        self.settings_lbl.setText(_translate("Dialog", "Tutaj znajdą się ustawienia użytkownika. Wszystkie ścieżki, dane ustawione tutaj - będą widnieć we wtyczce."))
        self.save_btn.setText(_translate("Dialog", "Zapisz"))
        self.reset_btn.setText(_translate("Dialog", "Resetuj"))
        self.cancel_btn.setText(_translate("Dialog", "Anuluj"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
