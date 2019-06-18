# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UpdateCamera.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1119, 834)
        Dialog.setMinimumSize(QtCore.QSize(1119, 834))
        Dialog.setMaximumSize(QtCore.QSize(1119, 834))
        self.buttonSaveConfiguration = QtWidgets.QPushButton(Dialog)
        self.buttonSaveConfiguration.setGeometry(QtCore.QRect(430, 770, 300, 51))
        self.buttonSaveConfiguration.setMinimumSize(QtCore.QSize(300, 51))
        self.buttonSaveConfiguration.setMaximumSize(QtCore.QSize(300, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.buttonSaveConfiguration.setFont(font)
        self.buttonSaveConfiguration.setObjectName("buttonSaveConfiguration")
        self.line_3 = QtWidgets.QFrame(Dialog)
        self.line_3.setGeometry(QtCore.QRect(670, 40, 31, 721))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(False)
        font.setWeight(50)
        self.line_3.setFont(font)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(720, 40, 111, 241))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(False)
        font.setWeight(50)
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelCameraName = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelCameraName.setFont(font)
        self.labelCameraName.setObjectName("labelCameraName")
        self.verticalLayout_2.addWidget(self.labelCameraName)
        self.labelCameraIP = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelCameraIP.setFont(font)
        self.labelCameraIP.setObjectName("labelCameraIP")
        self.verticalLayout_2.addWidget(self.labelCameraIP)
        self.labelCameraIPAddition = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelCameraIPAddition.setFont(font)
        self.labelCameraIPAddition.setObjectName("labelCameraIPAddition")
        self.verticalLayout_2.addWidget(self.labelCameraIPAddition)
        self.labelUserName = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelUserName.setFont(font)
        self.labelUserName.setObjectName("labelUserName")
        self.verticalLayout_2.addWidget(self.labelUserName)
        self.labelPassword = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelPassword.setFont(font)
        self.labelPassword.setObjectName("labelPassword")
        self.verticalLayout_2.addWidget(self.labelPassword)
        self.labelProtocolType = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelProtocolType.setFont(font)
        self.labelProtocolType.setObjectName("labelProtocolType")
        self.verticalLayout_2.addWidget(self.labelProtocolType)
        self.labelLocation = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelLocation.setFont(font)
        self.labelLocation.setObjectName("labelLocation")
        self.verticalLayout_2.addWidget(self.labelLocation)
        self.labelCalibrationPhoto = QtWidgets.QLabel(Dialog)
        self.labelCalibrationPhoto.setGeometry(QtCore.QRect(10, 40, 640, 480))
        self.labelCalibrationPhoto.setMinimumSize(QtCore.QSize(640, 480))
        self.labelCalibrationPhoto.setMaximumSize(QtCore.QSize(640, 480))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(False)
        font.setWeight(50)
        self.labelCalibrationPhoto.setFont(font)
        self.labelCalibrationPhoto.setStyleSheet("background-color: rgb(50,50,50)\n"
"\n"
"")
        self.labelCalibrationPhoto.setFrameShape(QtWidgets.QFrame.Box)
        self.labelCalibrationPhoto.setFrameShadow(QtWidgets.QFrame.Raised)
        self.labelCalibrationPhoto.setLineWidth(2)
        self.labelCalibrationPhoto.setText("")
        self.labelCalibrationPhoto.setObjectName("labelCalibrationPhoto")
        self.buttonShowContours = QtWidgets.QPushButton(Dialog)
        self.buttonShowContours.setGeometry(QtCore.QRect(190, 660, 281, 61))
        self.buttonShowContours.setMinimumSize(QtCore.QSize(281, 61))
        self.buttonShowContours.setMaximumSize(QtCore.QSize(281, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.buttonShowContours.setFont(font)
        self.buttonShowContours.setToolTipDuration(9999)
        self.buttonShowContours.setObjectName("buttonShowContours")
        self.labelCharReadingCalibration = QtWidgets.QLabel(Dialog)
        self.labelCharReadingCalibration.setGeometry(QtCore.QRect(780, 290, 311, 31))
        self.labelCharReadingCalibration.setMinimumSize(QtCore.QSize(141, 31))
        self.labelCharReadingCalibration.setMaximumSize(QtCore.QSize(400, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.labelCharReadingCalibration.setFont(font)
        self.labelCharReadingCalibration.setObjectName("labelCharReadingCalibration")
        self.layoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_3.setGeometry(QtCore.QRect(960, 330, 100, 411))
        self.layoutWidget_3.setMinimumSize(QtCore.QSize(100, 0))
        self.layoutWidget_3.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(False)
        font.setWeight(50)
        self.layoutWidget_3.setFont(font)
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.editMinPixelWidth = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMinPixelWidth.setMinimumSize(QtCore.QSize(90, 28))
        self.editMinPixelWidth.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMinPixelWidth.setFont(font)
        self.editMinPixelWidth.setToolTipDuration(9999)
        self.editMinPixelWidth.setText("")
        self.editMinPixelWidth.setClearButtonEnabled(True)
        self.editMinPixelWidth.setObjectName("editMinPixelWidth")
        self.verticalLayout_5.addWidget(self.editMinPixelWidth)
        self.editMinPixelHeight = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMinPixelHeight.setMinimumSize(QtCore.QSize(90, 28))
        self.editMinPixelHeight.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMinPixelHeight.setFont(font)
        self.editMinPixelHeight.setToolTipDuration(9999)
        self.editMinPixelHeight.setText("")
        self.editMinPixelHeight.setClearButtonEnabled(True)
        self.editMinPixelHeight.setObjectName("editMinPixelHeight")
        self.verticalLayout_5.addWidget(self.editMinPixelHeight)
        self.editMinPixelArea = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMinPixelArea.setMinimumSize(QtCore.QSize(90, 28))
        self.editMinPixelArea.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMinPixelArea.setFont(font)
        self.editMinPixelArea.setToolTipDuration(9999)
        self.editMinPixelArea.setClearButtonEnabled(True)
        self.editMinPixelArea.setObjectName("editMinPixelArea")
        self.verticalLayout_5.addWidget(self.editMinPixelArea)
        self.editMinPixelRatio = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMinPixelRatio.setMinimumSize(QtCore.QSize(90, 28))
        self.editMinPixelRatio.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMinPixelRatio.setFont(font)
        self.editMinPixelRatio.setToolTipDuration(9999)
        self.editMinPixelRatio.setText("")
        self.editMinPixelRatio.setClearButtonEnabled(True)
        self.editMinPixelRatio.setObjectName("editMinPixelRatio")
        self.verticalLayout_5.addWidget(self.editMinPixelRatio)
        self.editMaxPixelRatio = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMaxPixelRatio.setMinimumSize(QtCore.QSize(90, 28))
        self.editMaxPixelRatio.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMaxPixelRatio.setFont(font)
        self.editMaxPixelRatio.setToolTipDuration(9999)
        self.editMaxPixelRatio.setText("")
        self.editMaxPixelRatio.setClearButtonEnabled(True)
        self.editMaxPixelRatio.setObjectName("editMaxPixelRatio")
        self.verticalLayout_5.addWidget(self.editMaxPixelRatio)
        self.editMinDiagSize = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMinDiagSize.setMinimumSize(QtCore.QSize(90, 28))
        self.editMinDiagSize.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMinDiagSize.setFont(font)
        self.editMinDiagSize.setToolTipDuration(9999)
        self.editMinDiagSize.setText("")
        self.editMinDiagSize.setClearButtonEnabled(True)
        self.editMinDiagSize.setObjectName("editMinDiagSize")
        self.verticalLayout_5.addWidget(self.editMinDiagSize)
        self.editMaxDiagSize = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMaxDiagSize.setMinimumSize(QtCore.QSize(90, 28))
        self.editMaxDiagSize.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMaxDiagSize.setFont(font)
        self.editMaxDiagSize.setToolTipDuration(9999)
        self.editMaxDiagSize.setText("")
        self.editMaxDiagSize.setClearButtonEnabled(True)
        self.editMaxDiagSize.setObjectName("editMaxDiagSize")
        self.verticalLayout_5.addWidget(self.editMaxDiagSize)
        self.editMaxChangeInArea = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMaxChangeInArea.setMinimumSize(QtCore.QSize(90, 28))
        self.editMaxChangeInArea.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMaxChangeInArea.setFont(font)
        self.editMaxChangeInArea.setToolTipDuration(9999)
        self.editMaxChangeInArea.setText("")
        self.editMaxChangeInArea.setClearButtonEnabled(True)
        self.editMaxChangeInArea.setObjectName("editMaxChangeInArea")
        self.verticalLayout_5.addWidget(self.editMaxChangeInArea)
        self.editMaxChangeInWidth = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMaxChangeInWidth.setMinimumSize(QtCore.QSize(90, 28))
        self.editMaxChangeInWidth.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMaxChangeInWidth.setFont(font)
        self.editMaxChangeInWidth.setToolTipDuration(9999)
        self.editMaxChangeInWidth.setText("")
        self.editMaxChangeInWidth.setClearButtonEnabled(True)
        self.editMaxChangeInWidth.setObjectName("editMaxChangeInWidth")
        self.verticalLayout_5.addWidget(self.editMaxChangeInWidth)
        self.editMaxChangeInHeight = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMaxChangeInHeight.setMinimumSize(QtCore.QSize(90, 28))
        self.editMaxChangeInHeight.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMaxChangeInHeight.setFont(font)
        self.editMaxChangeInHeight.setToolTipDuration(9999)
        self.editMaxChangeInHeight.setText("")
        self.editMaxChangeInHeight.setClearButtonEnabled(True)
        self.editMaxChangeInHeight.setObjectName("editMaxChangeInHeight")
        self.verticalLayout_5.addWidget(self.editMaxChangeInHeight)
        self.editMaxAngleBetweenChar = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMaxAngleBetweenChar.setMinimumSize(QtCore.QSize(90, 28))
        self.editMaxAngleBetweenChar.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMaxAngleBetweenChar.setFont(font)
        self.editMaxAngleBetweenChar.setToolTipDuration(9999)
        self.editMaxAngleBetweenChar.setText("")
        self.editMaxAngleBetweenChar.setClearButtonEnabled(True)
        self.editMaxAngleBetweenChar.setObjectName("editMaxAngleBetweenChar")
        self.verticalLayout_5.addWidget(self.editMaxAngleBetweenChar)
        self.editMinNumberOfMatchCharNumber = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.editMinNumberOfMatchCharNumber.setMinimumSize(QtCore.QSize(90, 28))
        self.editMinNumberOfMatchCharNumber.setMaximumSize(QtCore.QSize(90, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editMinNumberOfMatchCharNumber.setFont(font)
        self.editMinNumberOfMatchCharNumber.setToolTipDuration(9999)
        self.editMinNumberOfMatchCharNumber.setText("")
        self.editMinNumberOfMatchCharNumber.setClearButtonEnabled(True)
        self.editMinNumberOfMatchCharNumber.setObjectName("editMinNumberOfMatchCharNumber")
        self.verticalLayout_5.addWidget(self.editMinNumberOfMatchCharNumber)
        self.layoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_4.setGeometry(QtCore.QRect(750, 330, 201, 401))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(False)
        font.setWeight(50)
        self.layoutWidget_4.setFont(font)
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget_4)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.labelMinPixelWidth = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMinPixelWidth.setFont(font)
        self.labelMinPixelWidth.setObjectName("labelMinPixelWidth")
        self.verticalLayout_6.addWidget(self.labelMinPixelWidth)
        self.labelMinPixelHeight = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMinPixelHeight.setFont(font)
        self.labelMinPixelHeight.setObjectName("labelMinPixelHeight")
        self.verticalLayout_6.addWidget(self.labelMinPixelHeight)
        self.labelMinPixelArea = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMinPixelArea.setFont(font)
        self.labelMinPixelArea.setObjectName("labelMinPixelArea")
        self.verticalLayout_6.addWidget(self.labelMinPixelArea)
        self.labelMinPixelRatio = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMinPixelRatio.setFont(font)
        self.labelMinPixelRatio.setObjectName("labelMinPixelRatio")
        self.verticalLayout_6.addWidget(self.labelMinPixelRatio)
        self.labelMaxPixelRatio = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMaxPixelRatio.setFont(font)
        self.labelMaxPixelRatio.setObjectName("labelMaxPixelRatio")
        self.verticalLayout_6.addWidget(self.labelMaxPixelRatio)
        self.labelMinDiagSize = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMinDiagSize.setFont(font)
        self.labelMinDiagSize.setObjectName("labelMinDiagSize")
        self.verticalLayout_6.addWidget(self.labelMinDiagSize)
        self.labelMaxDiagSize = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMaxDiagSize.setFont(font)
        self.labelMaxDiagSize.setObjectName("labelMaxDiagSize")
        self.verticalLayout_6.addWidget(self.labelMaxDiagSize)
        self.labelMaxChangeInArea = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMaxChangeInArea.setFont(font)
        self.labelMaxChangeInArea.setObjectName("labelMaxChangeInArea")
        self.verticalLayout_6.addWidget(self.labelMaxChangeInArea)
        self.labelMaxChangeInWidth = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMaxChangeInWidth.setFont(font)
        self.labelMaxChangeInWidth.setObjectName("labelMaxChangeInWidth")
        self.verticalLayout_6.addWidget(self.labelMaxChangeInWidth)
        self.labelMaChangeInHeight = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMaChangeInHeight.setFont(font)
        self.labelMaChangeInHeight.setObjectName("labelMaChangeInHeight")
        self.verticalLayout_6.addWidget(self.labelMaChangeInHeight)
        self.labelMaxAngleBetweenChar = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMaxAngleBetweenChar.setFont(font)
        self.labelMaxAngleBetweenChar.setObjectName("labelMaxAngleBetweenChar")
        self.verticalLayout_6.addWidget(self.labelMaxAngleBetweenChar)
        self.labelMinNumberOfMatchCharNumber = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelMinNumberOfMatchCharNumber.setFont(font)
        self.labelMinNumberOfMatchCharNumber.setObjectName("labelMinNumberOfMatchCharNumber")
        self.verticalLayout_6.addWidget(self.labelMinNumberOfMatchCharNumber)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(840, 40, 263, 241))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(False)
        font.setWeight(50)
        self.layoutWidget1.setFont(font)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.editCameraName = QtWidgets.QLineEdit(self.layoutWidget1)
        self.editCameraName.setMinimumSize(QtCore.QSize(261, 30))
        self.editCameraName.setMaximumSize(QtCore.QSize(261, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editCameraName.setFont(font)
        self.editCameraName.setToolTipDuration(9999)
        self.editCameraName.setText("")
        self.editCameraName.setClearButtonEnabled(True)
        self.editCameraName.setObjectName("editCameraName")
        self.verticalLayout_4.addWidget(self.editCameraName)
        self.editCameraIP = QtWidgets.QLineEdit(self.layoutWidget1)
        self.editCameraIP.setMinimumSize(QtCore.QSize(261, 30))
        self.editCameraIP.setMaximumSize(QtCore.QSize(261, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editCameraIP.setFont(font)
        self.editCameraIP.setToolTipDuration(9999)
        self.editCameraIP.setText("")
        self.editCameraIP.setClearButtonEnabled(True)
        self.editCameraIP.setObjectName("editCameraIP")
        self.verticalLayout_4.addWidget(self.editCameraIP)
        self.editCameraIPAddition = QtWidgets.QLineEdit(self.layoutWidget1)
        self.editCameraIPAddition.setMinimumSize(QtCore.QSize(261, 29))
        self.editCameraIPAddition.setMaximumSize(QtCore.QSize(261, 29))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editCameraIPAddition.setFont(font)
        self.editCameraIPAddition.setToolTipDuration(9999)
        self.editCameraIPAddition.setClearButtonEnabled(True)
        self.editCameraIPAddition.setObjectName("editCameraIPAddition")
        self.verticalLayout_4.addWidget(self.editCameraIPAddition)
        self.editUsername = QtWidgets.QLineEdit(self.layoutWidget1)
        self.editUsername.setMinimumSize(QtCore.QSize(261, 30))
        self.editUsername.setMaximumSize(QtCore.QSize(261, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editUsername.setFont(font)
        self.editUsername.setToolTipDuration(9999)
        self.editUsername.setText("")
        self.editUsername.setClearButtonEnabled(True)
        self.editUsername.setObjectName("editUsername")
        self.verticalLayout_4.addWidget(self.editUsername)
        self.editPassword = QtWidgets.QLineEdit(self.layoutWidget1)
        self.editPassword.setMinimumSize(QtCore.QSize(261, 30))
        self.editPassword.setMaximumSize(QtCore.QSize(261, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editPassword.setFont(font)
        self.editPassword.setToolTipDuration(9999)
        self.editPassword.setText("")
        self.editPassword.setClearButtonEnabled(True)
        self.editPassword.setObjectName("editPassword")
        self.verticalLayout_4.addWidget(self.editPassword)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButtonRtsp = QtWidgets.QRadioButton(self.layoutWidget1)
        self.radioButtonRtsp.setMinimumSize(QtCore.QSize(115, 22))
        self.radioButtonRtsp.setMaximumSize(QtCore.QSize(115, 22))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.radioButtonRtsp.setFont(font)
        self.radioButtonRtsp.setObjectName("radioButtonRtsp")
        self.horizontalLayout_2.addWidget(self.radioButtonRtsp)
        self.radioButtonHttp = QtWidgets.QRadioButton(self.layoutWidget1)
        self.radioButtonHttp.setMinimumSize(QtCore.QSize(114, 22))
        self.radioButtonHttp.setMaximumSize(QtCore.QSize(114, 22))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.radioButtonHttp.setFont(font)
        self.radioButtonHttp.setObjectName("radioButtonHttp")
        self.horizontalLayout_2.addWidget(self.radioButtonHttp)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.editLocation = QtWidgets.QLineEdit(self.layoutWidget1)
        self.editLocation.setMinimumSize(QtCore.QSize(261, 30))
        self.editLocation.setMaximumSize(QtCore.QSize(261, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editLocation.setFont(font)
        self.editLocation.setToolTipDuration(9999)
        self.editLocation.setText("")
        self.editLocation.setClearButtonEnabled(True)
        self.editLocation.setObjectName("editLocation")
        self.verticalLayout_4.addWidget(self.editLocation)
        self.layoutWidget2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget2.setGeometry(QtCore.QRect(750, 740, 351, 26))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelCameraStatus = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelCameraStatus.setFont(font)
        self.labelCameraStatus.setToolTipDuration(9999)
        self.labelCameraStatus.setObjectName("labelCameraStatus")
        self.horizontalLayout_4.addWidget(self.labelCameraStatus)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioButtonWorking = QtWidgets.QRadioButton(self.layoutWidget2)
        self.radioButtonWorking.setMinimumSize(QtCore.QSize(115, 22))
        self.radioButtonWorking.setMaximumSize(QtCore.QSize(115, 22))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.radioButtonWorking.setFont(font)
        self.radioButtonWorking.setObjectName("radioButtonWorking")
        self.horizontalLayout_3.addWidget(self.radioButtonWorking)
        self.radioButtonNotWorking = QtWidgets.QRadioButton(self.layoutWidget2)
        self.radioButtonNotWorking.setMinimumSize(QtCore.QSize(114, 22))
        self.radioButtonNotWorking.setMaximumSize(QtCore.QSize(114, 22))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.radioButtonNotWorking.setFont(font)
        self.radioButtonNotWorking.setObjectName("radioButtonNotWorking")
        self.horizontalLayout_3.addWidget(self.radioButtonNotWorking)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(360, 560, 272, 82))
        self.widget.setObjectName("widget")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.labelBottomY1 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelBottomY1.setFont(font)
        self.labelBottomY1.setObjectName("labelBottomY1")
        self.verticalLayout_11.addWidget(self.labelBottomY1)
        self.labelBottomY2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelBottomY2.setFont(font)
        self.labelBottomY2.setObjectName("labelBottomY2")
        self.verticalLayout_11.addWidget(self.labelBottomY2)
        self.horizontalLayout_8.addLayout(self.verticalLayout_11)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.editBottomY1 = QtWidgets.QLineEdit(self.widget)
        self.editBottomY1.setMinimumSize(QtCore.QSize(100, 36))
        self.editBottomY1.setMaximumSize(QtCore.QSize(100, 36))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editBottomY1.setFont(font)
        self.editBottomY1.setText("")
        self.editBottomY1.setClearButtonEnabled(True)
        self.editBottomY1.setObjectName("editBottomY1")
        self.verticalLayout_12.addWidget(self.editBottomY1)
        self.editBottomY2 = QtWidgets.QLineEdit(self.widget)
        self.editBottomY2.setMinimumSize(QtCore.QSize(100, 36))
        self.editBottomY2.setMaximumSize(QtCore.QSize(100, 36))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editBottomY2.setFont(font)
        self.editBottomY2.setText("")
        self.editBottomY2.setClearButtonEnabled(True)
        self.editBottomY2.setObjectName("editBottomY2")
        self.verticalLayout_12.addWidget(self.editBottomY2)
        self.horizontalLayout_8.addLayout(self.verticalLayout_12)
        self.widget1 = QtWidgets.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(30, 560, 275, 82))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.labelTopY1 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelTopY1.setFont(font)
        self.labelTopY1.setObjectName("labelTopY1")
        self.verticalLayout_3.addWidget(self.labelTopY1)
        self.labelTopY2 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelTopY2.setFont(font)
        self.labelTopY2.setObjectName("labelTopY2")
        self.verticalLayout_3.addWidget(self.labelTopY2)
        self.horizontalLayout_9.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.editTopY1 = QtWidgets.QLineEdit(self.widget1)
        self.editTopY1.setMinimumSize(QtCore.QSize(100, 36))
        self.editTopY1.setMaximumSize(QtCore.QSize(100, 36))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editTopY1.setFont(font)
        self.editTopY1.setText("")
        self.editTopY1.setClearButtonEnabled(True)
        self.editTopY1.setObjectName("editTopY1")
        self.verticalLayout.addWidget(self.editTopY1)
        self.editTopY2 = QtWidgets.QLineEdit(self.widget1)
        self.editTopY2.setMinimumSize(QtCore.QSize(100, 36))
        self.editTopY2.setMaximumSize(QtCore.QSize(100, 36))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.editTopY2.setFont(font)
        self.editTopY2.setText("")
        self.editTopY2.setClearButtonEnabled(True)
        self.editTopY2.setObjectName("editTopY2")
        self.verticalLayout.addWidget(self.editTopY2)
        self.horizontalLayout_9.addLayout(self.verticalLayout)
        self.widget2 = QtWidgets.QWidget(Dialog)
        self.widget2.setGeometry(QtCore.QRect(10, 0, 1101, 33))
        self.widget2.setObjectName("widget2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line = QtWidgets.QFrame(self.widget2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.labelCameraInfo = QtWidgets.QLabel(self.widget2)
        self.labelCameraInfo.setMinimumSize(QtCore.QSize(150, 31))
        self.labelCameraInfo.setMaximumSize(QtCore.QSize(150, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.labelCameraInfo.setFont(font)
        self.labelCameraInfo.setObjectName("labelCameraInfo")
        self.horizontalLayout.addWidget(self.labelCameraInfo)
        self.line_2 = QtWidgets.QFrame(self.widget2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.buttonSaveConfiguration.setText(_translate("Dialog", "KAMERA AYARINI KAYDET"))
        self.labelCameraName.setText(_translate("Dialog", "Kamera Adı"))
        self.labelCameraIP.setText(_translate("Dialog", "Kamera IP"))
        self.labelCameraIPAddition.setText(_translate("Dialog", "IP Ek Uzantı"))
        self.labelUserName.setText(_translate("Dialog", "Kullanıcı Adı"))
        self.labelPassword.setText(_translate("Dialog", "Şifre"))
        self.labelProtocolType.setText(_translate("Dialog", "Protokol Tipi"))
        self.labelLocation.setText(_translate("Dialog", "Konum"))
        self.buttonShowContours.setText(_translate("Dialog", "SINIRLARI GÖSTER"))
        self.labelCharReadingCalibration.setText(_translate("Dialog", "KARAKTER OKUMA KALİBRASYONU"))
        self.labelMinPixelWidth.setText(_translate("Dialog", "Min. Piksel Genişliği"))
        self.labelMinPixelHeight.setText(_translate("Dialog", "Min. Piksel Yüksekliği"))
        self.labelMinPixelArea.setText(_translate("Dialog", "Min. Piksel Alanı"))
        self.labelMinPixelRatio.setText(_translate("Dialog", "Min. Piksel Oranı"))
        self.labelMaxPixelRatio.setText(_translate("Dialog", "Max. Piksel Oranı"))
        self.labelMinDiagSize.setText(_translate("Dialog", "Min. Köşegen Boyutu Çarpanı"))
        self.labelMaxDiagSize.setText(_translate("Dialog", "Max. Köşegen Boyutu Çarpanı"))
        self.labelMaxChangeInArea.setText(_translate("Dialog", "Alandaki Max. Değişim"))
        self.labelMaxChangeInWidth.setText(_translate("Dialog", "Genişlikteki Max. Değişim"))
        self.labelMaChangeInHeight.setText(_translate("Dialog", "Yükseklikteki Max. Değişim"))
        self.labelMaxAngleBetweenChar.setText(_translate("Dialog", "Karakterler Arası Max. Açı"))
        self.labelMinNumberOfMatchCharNumber.setText(_translate("Dialog", "Okunacak Min. Karakter Sayısı"))
        self.radioButtonRtsp.setText(_translate("Dialog", "RTSP"))
        self.radioButtonHttp.setText(_translate("Dialog", "HTTP"))
        self.labelCameraStatus.setText(_translate("Dialog", "Kamera Durumu"))
        self.radioButtonWorking.setText(_translate("Dialog", "Çalışıyor"))
        self.radioButtonNotWorking.setText(_translate("Dialog", "Çalışmıyor"))
        self.labelBottomY1.setText(_translate("Dialog", "ALT BÖLME İÇİN ÜST SINIR"))
        self.labelBottomY2.setText(_translate("Dialog", "ALT BÖLME İÇİN ALT SINIR"))
        self.labelTopY1.setText(_translate("Dialog", "ÜST BÖLME İÇİN ÜST SINIR"))
        self.labelTopY2.setText(_translate("Dialog", "ÜST BÖLME İÇİN ALT SINIR"))
        self.labelCameraInfo.setText(_translate("Dialog", "KAMERAYI GÜNCELLE"))


