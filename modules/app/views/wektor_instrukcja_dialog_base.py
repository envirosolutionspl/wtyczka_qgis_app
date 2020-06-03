# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wektor_instrukcja_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(580, 394)
        Dialog.setSizeGripEnabled(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 558, 215))
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
        self.empty1_lbl = QtWidgets.QLabel(Dialog)
        self.empty1_lbl.setText("")
        self.empty1_lbl.setObjectName("empty1_lbl")
        self.verticalLayout.addWidget(self.empty1_lbl)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addAppShp_lbl = QtWidgets.QLabel(Dialog)
        self.addAppShp_lbl.setObjectName("addAppShp_lbl")
        self.horizontalLayout.addWidget(self.addAppShp_lbl)
        self.addFile_widget = QgsFileWidget(Dialog)
        self.addFile_widget.setObjectName("addFile_widget")
        self.horizontalLayout.addWidget(self.addFile_widget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.empty2_lbl = QtWidgets.QLabel(Dialog)
        self.empty2_lbl.setText("")
        self.empty2_lbl.setObjectName("empty2_lbl")
        self.verticalLayout.addWidget(self.empty2_lbl)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.prev_btn = QtWidgets.QPushButton(Dialog)
        self.prev_btn.setEnabled(True)
        self.prev_btn.setObjectName("prev_btn")
        self.horizontalLayout_2.addWidget(self.prev_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.generateTemporaryLayer_btn = QtWidgets.QPushButton(Dialog)
        self.generateTemporaryLayer_btn.setObjectName("generateTemporaryLayer_btn")
        self.horizontalLayout_2.addWidget(self.generateTemporaryLayer_btn)
        self.saveLayer_btn = QtWidgets.QPushButton(Dialog)
        self.saveLayer_btn.setObjectName("saveLayer_btn")
        self.horizontalLayout_2.addWidget(self.saveLayer_btn)
        self.next_btn = QtWidgets.QPushButton(Dialog)
        self.next_btn.setObjectName("next_btn")
        self.horizontalLayout_2.addWidget(self.next_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_lbl.setText(_translate("Dialog", "Przygotowanie granic APP"))
        self.instruction_lbl.setText(_translate("Dialog", "Instrukcja tworzenia pliku wektorowego (wektoryzacja, odniesienia do narzędzi QGIS, link do filmiku instruktażowego, przypomnienie o zapisie edytowanej warstwy oraz o sposobie jej odtworzenia we wtyczce w przypadku wyjścia z QGIS)."))
        self.addAppShp_lbl.setText(_translate("Dialog", "Istniejący plik z granicami obowiązywania APP (opcjonalne)"))
        self.prev_btn.setText(_translate("Dialog", "Wstecz"))
        self.generateTemporaryLayer_btn.setText(_translate("Dialog", "Generuj warstwę tymczasową"))
        self.saveLayer_btn.setText(_translate("Dialog", "Zapisz warstwę"))
        self.next_btn.setText(_translate("Dialog", "Dalej"))
from qgsfilewidget import QgsFileWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
