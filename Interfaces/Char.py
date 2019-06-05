# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Char.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(216, 95)
        Dialog.setMinimumSize(QtCore.QSize(216, 95))
        Dialog.setMaximumSize(QtCore.QSize(216, 95))
        Dialog.setMouseTracking(False)
        self.buttonAccept = QtWidgets.QPushButton(Dialog)
        self.buttonAccept.setGeometry(QtCore.QRect(30, 50, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.buttonAccept.setFont(font)
        self.buttonAccept.setObjectName("buttonAccept")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 201, 33))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(False)
        font.setWeight(50)
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setMinimumSize(QtCore.QSize(120, 31))
        self.label.setMaximumSize(QtCore.QSize(141, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.editChar = QtWidgets.QLineEdit(self.layoutWidget)
        self.editChar.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.editChar.setFont(font)
        self.editChar.setToolTipDuration(9999)
        self.editChar.setObjectName("editChar")
        self.horizontalLayout.addWidget(self.editChar)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.buttonAccept.setText(_translate("Dialog", "ONAYLA"))
        self.label.setText(_translate("Dialog", "SEÇİLİ KARAKTER"))


