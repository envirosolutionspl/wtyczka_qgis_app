# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formularz_dokumenty_dialog_base.ui'
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
        self.instruction_scrollArea = QtWidgets.QScrollArea(Dialog)
        self.instruction_scrollArea.setWidgetResizable(True)
        self.instruction_scrollArea.setObjectName("instruction_scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 478, 218))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.instruction_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.instruction_lbl.setFont(font)
        self.instruction_lbl.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.instruction_lbl.setWordWrap(True)
        self.instruction_lbl.setObjectName("instruction_lbl")
        self.gridLayout.addWidget(self.instruction_lbl, 0, 0, 1, 1)
        self.instruction_scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.instruction_scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.getValues_btn = QtWidgets.QPushButton(Dialog)
        self.getValues_btn.setObjectName("getValues_btn")
        self.horizontalLayout.addWidget(self.getValues_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.clear_btn = QtWidgets.QPushButton(Dialog)
        self.clear_btn.setObjectName("clear_btn")
        self.horizontalLayout.addWidget(self.clear_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.titleForm_lbl = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.titleForm_lbl.setFont(font)
        self.titleForm_lbl.setObjectName("titleForm_lbl")
        self.verticalLayout.addWidget(self.titleForm_lbl)
        self.form_scrollArea = QtWidgets.QScrollArea(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.form_scrollArea.sizePolicy().hasHeightForWidth())
        self.form_scrollArea.setSizePolicy(sizePolicy)
        self.form_scrollArea.setWidgetResizable(True)
        self.form_scrollArea.setObjectName("form_scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 478, 218))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tytul_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.tytul_lineEdit.setFont(font)
        self.tytul_lineEdit.setObjectName("tytul_lineEdit")
        self.gridLayout_2.addWidget(self.tytul_lineEdit, 2, 1, 1, 2)
        self.idHelp_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.idHelp_btn.setFont(font)
        self.idHelp_btn.setObjectName("idHelp_btn")
        self.gridLayout_2.addWidget(self.idHelp_btn, 0, 4, 1, 1)
        self.id_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.id_lineEdit.sizePolicy().hasHeightForWidth())
        self.id_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.id_lineEdit.setFont(font)
        self.id_lineEdit.setObjectName("id_lineEdit")
        self.gridLayout_2.addWidget(self.id_lineEdit, 0, 1, 1, 2)
        self.dziennikUrzedowy_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.dziennikUrzedowy_lineEdit.setFont(font)
        self.dziennikUrzedowy_lineEdit.setObjectName("dziennikUrzedowy_lineEdit")
        self.gridLayout_2.addWidget(self.dziennikUrzedowy_lineEdit, 4, 1, 1, 2)
        self.nazwaSkrocona_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.nazwaSkrocona_lineEdit.setFont(font)
        self.nazwaSkrocona_lineEdit.setObjectName("nazwaSkrocona_lineEdit")
        self.gridLayout_2.addWidget(self.nazwaSkrocona_lineEdit, 3, 1, 1, 2)
        self.tytul_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.tytul_lbl.setObjectName("tytul_lbl")
        self.gridLayout_2.addWidget(self.tytul_lbl, 2, 0, 1, 1)
        self.tytulHelp_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.tytulHelp_btn.setFont(font)
        self.tytulHelp_btn.setObjectName("tytulHelp_btn")
        self.gridLayout_2.addWidget(self.tytulHelp_btn, 2, 4, 1, 1)
        self.dziennikUrzedowy_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.dziennikUrzedowy_lbl.setObjectName("dziennikUrzedowy_lbl")
        self.gridLayout_2.addWidget(self.dziennikUrzedowy_lbl, 4, 0, 1, 1)
        self.nazwaSkroconaHelp_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.nazwaSkroconaHelp_btn.setFont(font)
        self.nazwaSkroconaHelp_btn.setObjectName("nazwaSkroconaHelp_btn")
        self.gridLayout_2.addWidget(self.nazwaSkroconaHelp_btn, 3, 4, 1, 1)
        self.nazwaSkrocona_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.nazwaSkrocona_lbl.setObjectName("nazwaSkrocona_lbl")
        self.gridLayout_2.addWidget(self.nazwaSkrocona_lbl, 3, 0, 1, 1)
        self.id_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.id_lbl.setObjectName("id_lbl")
        self.gridLayout_2.addWidget(self.id_lbl, 0, 0, 1, 1)
        self.dziennikUrzedowyHelp_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.dziennikUrzedowyHelp_btn.setFont(font)
        self.dziennikUrzedowyHelp_btn.setObjectName("dziennikUrzedowyHelp_btn")
        self.gridLayout_2.addWidget(self.dziennikUrzedowyHelp_btn, 4, 4, 1, 1)
        self.lacze_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.lacze_lbl.setObjectName("lacze_lbl")
        self.gridLayout_2.addWidget(self.lacze_lbl, 5, 0, 1, 1)
        self.lacze_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.lacze_lineEdit.setFont(font)
        self.lacze_lineEdit.setObjectName("lacze_lineEdit")
        self.gridLayout_2.addWidget(self.lacze_lineEdit, 5, 1, 1, 1)
        self.laczeHelp_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.laczeHelp_btn.setFont(font)
        self.laczeHelp_btn.setObjectName("laczeHelp_btn")
        self.gridLayout_2.addWidget(self.laczeHelp_btn, 5, 4, 1, 1)
        self.form_scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.form_scrollArea)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.prev_btn = QtWidgets.QPushButton(Dialog)
        self.prev_btn.setEnabled(True)
        self.prev_btn.setObjectName("prev_btn")
        self.horizontalLayout_2.addWidget(self.prev_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.saveForm_btn = QtWidgets.QPushButton(Dialog)
        self.saveForm_btn.setObjectName("saveForm_btn")
        self.horizontalLayout_2.addWidget(self.saveForm_btn)
        self.next_btn = QtWidgets.QPushButton(Dialog)
        self.next_btn.setObjectName("next_btn")
        self.horizontalLayout_2.addWidget(self.next_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_lbl.setText(_translate("Dialog", "Formularz atrybutów dla dokumentów formalnych"))
        self.instruction_lbl.setText(_translate("Dialog", "Instrukcja jak poprawnie wypełnić formularz atrybutów. Możliwość wielokrotnego wypełnienia formularza. Co najmniej jeden formularz musi zostać wygenerowany dla danego APP."))
        self.getValues_btn.setText(_translate("Dialog", "Pobierz wartości z istniejącego formularza"))
        self.clear_btn.setText(_translate("Dialog", "Wyczyść formularz"))
        self.titleForm_lbl.setText(_translate("Dialog", "Formularz atrybutów:"))
        self.idHelp_btn.setText(_translate("Dialog", "?"))
        self.tytul_lbl.setText(_translate("Dialog", "tytul"))
        self.tytulHelp_btn.setText(_translate("Dialog", "?"))
        self.dziennikUrzedowy_lbl.setText(_translate("Dialog", "dziennikUrzedowy"))
        self.nazwaSkroconaHelp_btn.setText(_translate("Dialog", "?"))
        self.nazwaSkrocona_lbl.setText(_translate("Dialog", "nazwaSkrocona"))
        self.id_lbl.setText(_translate("Dialog", "idIIP"))
        self.dziennikUrzedowyHelp_btn.setText(_translate("Dialog", "?"))
        self.lacze_lbl.setText(_translate("Dialog", "lacze"))
        self.laczeHelp_btn.setText(_translate("Dialog", "?"))
        self.prev_btn.setText(_translate("Dialog", "Wstecz"))
        self.saveForm_btn.setText(_translate("Dialog", "Zapisz aktualny formularz"))
        self.next_btn.setText(_translate("Dialog", "Dalej"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())