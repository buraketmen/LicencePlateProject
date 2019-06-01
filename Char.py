# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Char.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(221, 102)
        Dialog.setMouseTracking(False)
        self.buttonAccept = QtWidgets.QPushButton(Dialog)
        self.buttonAccept.setGeometry(QtCore.QRect(20, 50, 161, 41))
        self.buttonAccept.setObjectName("buttonAccept")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 201, 31))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(141, 31))
        self.label.setMaximumSize(QtCore.QSize(141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.editChar = QtWidgets.QLineEdit(self.widget)
        self.editChar.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.editChar.setFont(font)
        self.editChar.setObjectName("editChar")
        self.horizontalLayout.addWidget(self.editChar)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.buttonAccept.setText(_translate("Dialog", "ONAYLA"))
        self.label.setText(_translate("Dialog", "SEÇİLİ KARAKTER"))


