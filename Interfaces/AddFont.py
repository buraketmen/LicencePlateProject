# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddFont.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(1169, 760)
        Dialog.setMinimumSize(QtCore.QSize(1169, 760))
        Dialog.setMaximumSize(QtCore.QSize(1169, 760))
        Dialog.setInputMethodHints(QtCore.Qt.ImhNone)
        Dialog.setSizeGripEnabled(False)
        self.line_3 = QtWidgets.QFrame(Dialog)
        self.line_3.setGeometry(QtCore.QRect(810, 40, 31, 601))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.line_3.setFont(font)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.labelFontPhoto = QtWidgets.QLabel(Dialog)
        self.labelFontPhoto.setGeometry(QtCore.QRect(10, 40, 800, 600))
        self.labelFontPhoto.setMinimumSize(QtCore.QSize(800, 600))
        self.labelFontPhoto.setMaximumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.labelFontPhoto.setFont(font)
        self.labelFontPhoto.setStyleSheet("background-color: rgb(50,50,50)\n"
"")
        self.labelFontPhoto.setFrameShape(QtWidgets.QFrame.Box)
        self.labelFontPhoto.setFrameShadow(QtWidgets.QFrame.Raised)
        self.labelFontPhoto.setLineWidth(3)
        self.labelFontPhoto.setText("")
        self.labelFontPhoto.setObjectName("labelFontPhoto")
        self.labelOriginalCroppedChar = QtWidgets.QLabel(Dialog)
        self.labelOriginalCroppedChar.setGeometry(QtCore.QRect(840, 100, 311, 261))
        self.labelOriginalCroppedChar.setMinimumSize(QtCore.QSize(311, 261))
        self.labelOriginalCroppedChar.setMaximumSize(QtCore.QSize(999, 999))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.labelOriginalCroppedChar.setFont(font)
        self.labelOriginalCroppedChar.setStyleSheet("background-color: rgb(50,50,50)\n"
"")
        self.labelOriginalCroppedChar.setFrameShape(QtWidgets.QFrame.Box)
        self.labelOriginalCroppedChar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.labelOriginalCroppedChar.setLineWidth(3)
        self.labelOriginalCroppedChar.setText("")
        self.labelOriginalCroppedChar.setObjectName("labelOriginalCroppedChar")
        self.labelThreshCroppedChar = QtWidgets.QLabel(Dialog)
        self.labelThreshCroppedChar.setGeometry(QtCore.QRect(840, 380, 311, 261))
        self.labelThreshCroppedChar.setMinimumSize(QtCore.QSize(311, 261))
        self.labelThreshCroppedChar.setMaximumSize(QtCore.QSize(181, 201))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.labelThreshCroppedChar.setFont(font)
        self.labelThreshCroppedChar.setStyleSheet("background-color: rgb(50,50,50)\n"
"")
        self.labelThreshCroppedChar.setFrameShape(QtWidgets.QFrame.Box)
        self.labelThreshCroppedChar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.labelThreshCroppedChar.setLineWidth(3)
        self.labelThreshCroppedChar.setText("")
        self.labelThreshCroppedChar.setObjectName("labelThreshCroppedChar")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 1141, 33))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.line = QtWidgets.QFrame(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.line.setFont(font)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.labelAddFont = QtWidgets.QLabel(self.layoutWidget)
        self.labelAddFont.setMinimumSize(QtCore.QSize(101, 31))
        self.labelAddFont.setMaximumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(17)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.labelAddFont.setFont(font)
        self.labelAddFont.setObjectName("labelAddFont")
        self.horizontalLayout_2.addWidget(self.labelAddFont)
        self.line_2 = QtWidgets.QFrame(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.line_2.setFont(font)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.buttonStartRecording = QtWidgets.QPushButton(Dialog)
        self.buttonStartRecording.setGeometry(QtCore.QRect(390, 700, 411, 51))
        self.buttonStartRecording.setMinimumSize(QtCore.QSize(261, 51))
        self.buttonStartRecording.setMaximumSize(QtCore.QSize(999, 999))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.buttonStartRecording.setFont(font)
        self.buttonStartRecording.setToolTipDuration(9999)
        self.buttonStartRecording.setObjectName("buttonStartRecording")
        self.buttonAddPhoto = QtWidgets.QPushButton(Dialog)
        self.buttonAddPhoto.setGeometry(QtCore.QRect(260, 650, 300, 41))
        self.buttonAddPhoto.setMinimumSize(QtCore.QSize(300, 30))
        self.buttonAddPhoto.setMaximumSize(QtCore.QSize(300, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.buttonAddPhoto.setFont(font)
        self.buttonAddPhoto.setObjectName("buttonAddPhoto")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(840, 60, 311, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.splitter.setFont(font)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.labelFontName = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelFontName.setFont(font)
        self.labelFontName.setObjectName("labelFontName")
        self.editFontName = QtWidgets.QLineEdit(self.splitter)
        self.editFontName.setMinimumSize(QtCore.QSize(230, 30))
        self.editFontName.setMaximumSize(QtCore.QSize(230, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.editFontName.setFont(font)
        self.editFontName.setToolTipDuration(9999)
        self.editFontName.setInputMethodHints(QtCore.Qt.ImhNone)
        self.editFontName.setText("")
        self.editFontName.setMaxLength(30)
        self.editFontName.setFrame(True)
        self.editFontName.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.editFontName.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.editFontName.setClearButtonEnabled(True)
        self.editFontName.setObjectName("editFontName")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelAddFont.setText(_translate("Dialog", "FONT EKLE"))
        self.buttonStartRecording.setText(_translate("Dialog", "KAYIT İŞLEMİNE BAŞLA"))
        self.buttonAddPhoto.setText(_translate("Dialog", "FONT FOTOĞRAFI YÜKLE"))
        self.labelFontName.setText(_translate("Dialog", "Font Adı"))


