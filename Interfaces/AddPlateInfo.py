# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddPlateInfo.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(445, 333)
        Dialog.setMinimumSize(QtCore.QSize(445, 333))
        Dialog.setMaximumSize(QtCore.QSize(445, 333))
        self.buttonSave = QtWidgets.QPushButton(Dialog)
        self.buttonSave.setGeometry(QtCore.QRect(100, 270, 261, 51))
        self.buttonSave.setMinimumSize(QtCore.QSize(261, 51))
        self.buttonSave.setMaximumSize(QtCore.QSize(261, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.buttonSave.setFont(font)
        self.buttonSave.setObjectName("buttonSave")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 50, 266, 211))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTopCharCount = QtWidgets.QLabel(self.layoutWidget)
        self.labelTopCharCount.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelTopCharCount.setFont(font)
        self.labelTopCharCount.setObjectName("labelTopCharCount")
        self.verticalLayout.addWidget(self.labelTopCharCount)
        self.labelTopMinCharCount = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelTopMinCharCount.setFont(font)
        self.labelTopMinCharCount.setObjectName("labelTopMinCharCount")
        self.verticalLayout.addWidget(self.labelTopMinCharCount)
        self.labelBottomCharCount = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelBottomCharCount.setFont(font)
        self.labelBottomCharCount.setObjectName("labelBottomCharCount")
        self.verticalLayout.addWidget(self.labelBottomCharCount)
        self.labelBottomMinCharCount = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelBottomMinCharCount.setFont(font)
        self.labelBottomMinCharCount.setObjectName("labelBottomMinCharCount")
        self.verticalLayout.addWidget(self.labelBottomMinCharCount)
        self.labelControlCount = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelControlCount.setFont(font)
        self.labelControlCount.setObjectName("labelControlCount")
        self.verticalLayout.addWidget(self.labelControlCount)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(11, 1, 421, 33))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.layoutWidget1.setFont(font)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.line = QtWidgets.QFrame(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.line.setFont(font)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.labelPlateConfig = QtWidgets.QLabel(self.layoutWidget1)
        self.labelPlateConfig.setMinimumSize(QtCore.QSize(0, 0))
        self.labelPlateConfig.setMaximumSize(QtCore.QSize(120, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.labelPlateConfig.setFont(font)
        self.labelPlateConfig.setObjectName("labelPlateConfig")
        self.horizontalLayout_2.addWidget(self.labelPlateConfig)
        self.line_2 = QtWidgets.QFrame(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.line_2.setFont(font)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.layoutWidget2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget2.setGeometry(QtCore.QRect(270, 50, 151, 206))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.layoutWidget2.setFont(font)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.editTopCharCount = QtWidgets.QLineEdit(self.layoutWidget2)
        self.editTopCharCount.setMinimumSize(QtCore.QSize(50, 36))
        self.editTopCharCount.setMaximumSize(QtCore.QSize(261, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.editTopCharCount.setFont(font)
        self.editTopCharCount.setToolTipDuration(9999)
        self.editTopCharCount.setText("")
        self.editTopCharCount.setClearButtonEnabled(True)
        self.editTopCharCount.setObjectName("editTopCharCount")
        self.verticalLayout_2.addWidget(self.editTopCharCount)
        self.editTopMinCharCount = QtWidgets.QLineEdit(self.layoutWidget2)
        self.editTopMinCharCount.setMinimumSize(QtCore.QSize(50, 36))
        self.editTopMinCharCount.setMaximumSize(QtCore.QSize(261, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.editTopMinCharCount.setFont(font)
        self.editTopMinCharCount.setToolTipDuration(9999)
        self.editTopMinCharCount.setText("")
        self.editTopMinCharCount.setClearButtonEnabled(True)
        self.editTopMinCharCount.setObjectName("editTopMinCharCount")
        self.verticalLayout_2.addWidget(self.editTopMinCharCount)
        self.editBottomCharCount = QtWidgets.QLineEdit(self.layoutWidget2)
        self.editBottomCharCount.setMinimumSize(QtCore.QSize(50, 36))
        self.editBottomCharCount.setMaximumSize(QtCore.QSize(261, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.editBottomCharCount.setFont(font)
        self.editBottomCharCount.setToolTipDuration(9999)
        self.editBottomCharCount.setClearButtonEnabled(True)
        self.editBottomCharCount.setObjectName("editBottomCharCount")
        self.verticalLayout_2.addWidget(self.editBottomCharCount)
        self.editBottomMinCharCount = QtWidgets.QLineEdit(self.layoutWidget2)
        self.editBottomMinCharCount.setMinimumSize(QtCore.QSize(50, 36))
        self.editBottomMinCharCount.setMaximumSize(QtCore.QSize(261, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.editBottomMinCharCount.setFont(font)
        self.editBottomMinCharCount.setToolTipDuration(9999)
        self.editBottomMinCharCount.setClearButtonEnabled(True)
        self.editBottomMinCharCount.setObjectName("editBottomMinCharCount")
        self.verticalLayout_2.addWidget(self.editBottomMinCharCount)
        self.editControlCount = QtWidgets.QLineEdit(self.layoutWidget2)
        self.editControlCount.setMinimumSize(QtCore.QSize(50, 36))
        self.editControlCount.setMaximumSize(QtCore.QSize(261, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.editControlCount.setFont(font)
        self.editControlCount.setToolTip("")
        self.editControlCount.setToolTipDuration(9999)
        self.editControlCount.setClearButtonEnabled(True)
        self.editControlCount.setObjectName("editControlCount")
        self.verticalLayout_2.addWidget(self.editControlCount)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.buttonSave.setText(_translate("Dialog", "KAYDET"))
        self.labelTopCharCount.setText(_translate("Dialog", "Üst Kısım Karakter Sayısı"))
        self.labelTopMinCharCount.setText(_translate("Dialog", "Üst Kısım Min. Karakter Sayısı"))
        self.labelBottomCharCount.setText(_translate("Dialog", "Alt Kısım Karakter Sayısı"))
        self.labelBottomMinCharCount.setText(_translate("Dialog", "Alt Kısım Min. Karakter Sayısı"))
        self.labelControlCount.setText(_translate("Dialog", "Kontrol Sayısı"))
        self.labelPlateConfig.setText(_translate("Dialog", "PLAKA AYARI"))


