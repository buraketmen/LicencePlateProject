import os
import cv2
from imutils.video import VideoStream
import imutils
import datetime
import locale
import base64
import numpy as np
import DetectChars
import DetectPlates
import PossiblePlate
import Database
import datetime
import shutil
import functools
from Interfaces.Cameras import Ui_Dialog
import Interfaces.Fonts as Fonts
import Interfaces.AddCamera as AddCamera
import Interfaces.AddFont as AddFont
import Interfaces.UpdateCamera as UpdateCamera
import Interfaces.Char as Char
import Interfaces.AddPlateInfo as AddPlateInfo
from Interfaces.GUI import Ui_MainWindow
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt, QRegExp
from PyQt5.QtGui import QImage, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem,QTableWidgetItem, QFileDialog, QWidget
import sqlite3
import DetectPlateThread
import threading
import multiprocessing
import time as t
import requests
from pythonping import ping

locale.setlocale(locale.LC_ALL, '')
conn = sqlite3.connect('PlateDetectionDB.db', check_same_thread=False)
curs = conn.cursor()

path = os.getcwd() + "\\"
path = str(path)
frameSize = (640, 480)

def GetPing(ip):
    try:
        response = ping(ip, size=5, count=1)
        if(str(response)[0:7]=="Request"):
            return False
        else:
            return True
    except Exception as error:
        date = GetDate()
        filename = path + "Log\\" + date
        logToday = open(filename, "a+")
        logToday.write(str(error)+ "\n")
        logToday.close()

def GetDate():
    an = datetime.datetime.now()
    second = int(an.second)
    hour = int(an.hour)
    date = str(an.day) + "." + str(an.month) + "." + str(an.year) + ".txt"
    return date

##############################################################################################
class WagonTracking(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(WagonTracking,self).__init__(parent)
        self.setupUi(self)
        self.capture = None
        self.image = None
        self.char = None
        self.fontPhoto = None
        self.checkPlateTop = None
        self.fname = None
        self.checkPlateBottom = None
        self.txtClass = None
        self.cameraStatus = False
        self.checkTop = 0
        self.checkBottom = 0
        self.backimage = cv2.imread(path + '\\Fonts\\background.png')
        self.listCamera = []
        self.InitUi()
        self.UpdateStatusBar()

    def InitUi(self):
        self.show()
        Database.setDatabase()
        comboboxThread = threading.Thread(target=self.FillComboBox)
        comboboxThread.daemon = True
        comboboxThread.start()

        cloudDBThread = threading.Thread(target= self.SendToCloud)
        cloudDBThread.daemon = True
        cloudDBThread.start()

        #conn.execute("DELETE FROM Plates")
        #conn.commit()
        #txtfile = open("ThreadStatus.txt", "w")
        #txtfile.write("True")
        self.LoadDatabase()
        self.startButton.clicked.connect(self.StartWebcam)
        self.startButton.setEnabled(True)
        self.stopButton.clicked.connect(self.StopWebcam)
        self.stopButton.setEnabled(False)
        self.detectButton.toggled.connect(self.DetectWebcam)
        self.detectButton.setCheckable(True)
        self.plateEnabled = False
        self.trainButton.clicked.connect(self.TrainPlates)
        self.plateTrain =False
        self.actionCameras.triggered.connect(self.ShowCamerasPage)
        self.actionAddCamera.triggered.connect(self.ShowAddCameraPage)
        self.actionFonts.triggered.connect(self.ShowFontsPage)
        self.actionAddFont.triggered.connect(self.ShowAddFont)
        self.actionPlate.triggered.connect(self.ShowAddPlateInfoPage)
        self.ComboBoxCameras.setEnabled(True)
        self.detectButton.setEnabled(False)

    def LoadDatabaseTable(self):
        self.LoadDatabase()

    def SendToCloud(self):
        while True:
            sent = "Hayır"
            searchall = conn.execute("SELECT Plate, Date, Time, Camera FROM Plates WHERE Sent =? ", (sent,))
            rows = searchall.fetchall()
            if (rows != None):
                for row in rows:
                    plate = str(row[0])
                    date = str(row[1])
                    fulltime = str(row[2])
                    timelist = fulltime.split(":")
                    time = timelist[0] + ":" + timelist[1]
                    camera = str(row[3])
                    search = conn.execute('SELECT CameraLocation FROM Cameras WHERE CameraName = ? ', (camera,))
                    result = search.fetchone()
                    if (result != None):
                        location = str(result[0])

                    
                    postUrl = "http://localhost:64738/api/v1/Plates/CreatePlate"
                    hed = {'Authorization': 'Bearer ' + token}
                    try:
                        response = requests.post(postUrl, timeout=5, json={"plate": str(plate),
                                                                           "camera": str(camera), "date": str(date),
                                                                           "time": str(time),
                                                                           "location": str(location)}, headers=hed)
                        r = response.json()
                        stringR = str(r)
                        if (stringR[14:18] == "True"):
                            print("aaa")
                            sent = "Evet"
                            conn.execute(
                                """UPDATE Plates SET Plate = ?, Date = ? , Time = ?, Camera = ? , Sent = ? WHERE Plate = ?""",
                                (plate, date, fulltime, camera, sent, plate))
                            conn.commit()
                    except:
                        pass
            t.sleep(5)


    def UpdateStatusBar(self):
        self.statusbar.show()
        self.statusbar.showMessage("Program kullanılmaya hazır.")
        self.startButton.setStatusTip("Kameraları başlatmak için tıkla.")
        self.stopButton.setStatusTip("Kamerayı durdurmak için tıkla.")
        self.trainButton.setStatusTip("Plaka tanıma için gerekli algoritmayı sisteme yükler.")
        self.detectButton.setStatusTip("Çalışır haldeki tüm kameralarda plaka tanımayı başlatmak için tıkla. Aktif hale gelmesi için KNN taraması yapılmalı. (Kamera IP bilgileri yanlışsa tarama yapılmayacaktır.)")
        self.tableWidget.setStatusTip("Kameralarda görünen ve veritabanına kaydedilen plakalar yer alır.")
        self.tableWidget_2.setStatusTip("Listeden seçilen kamerada okunan tüm veriler yer alır.")
        self.ComboBoxCameras.setStatusTip("Sistemde var olan ve çalışır durumdaki kameralar yer alır.")

    def FillComboBox(self):
        try:
            cameraStat = "Çalışıyor"
            while True:
                if (self.cameraStatus == False):
                    listofCameras = []
                    searchall = curs.execute('SELECT CameraName FROM Cameras WHERE CameraStatus = ?', (cameraStat,))
                    rows = searchall.fetchall()
                    if (len(rows) != 0):
                        for row in rows:
                            listofCameras.append(row[0])
                        if (self.listCamera != listofCameras):
                            del self.listCamera
                            self.listCamera = listofCameras.copy()
                            self.ComboBoxCameras.clear()
                            self.ComboBoxCameras.addItems(self.listCamera)
                    else:
                        self.ComboBoxCameras.clear()
                    t.sleep(10)
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error)+ "\n")
            logToday.close()


    def ShowAddPlateInfoPage(self):
        self.AddPlateInfo = AddPlateInfo()
        regexint = QRegExp("[0-9_]+")
        validatorint = QRegExpValidator(regexint)
        self.AddPlateInfo.editBottomCharCount.setValidator(validatorint)
        self.AddPlateInfo.editBottomMinCharCount.setValidator(validatorint)
        self.AddPlateInfo.editTopCharCount.setValidator(validatorint)
        self.AddPlateInfo.editTopMinCharCount.setValidator(validatorint)
        self.AddPlateInfo.editControlCount.setValidator(validatorint)
        self.AddPlateInfo.buttonSave.clicked.connect(self.SavePlateInfo)
        try:
            plateinfo = open("PlateInfo.txt", "r")
            line = str(plateinfo.readline())
            counts = line.split(",")
            self.AddPlateInfo.editTopCharCount.setText(counts[0])
            self.AddPlateInfo.editTopMinCharCount.setText(counts[1])
            self.AddPlateInfo.editBottomCharCount.setText(counts[2])
            self.AddPlateInfo.editBottomMinCharCount.setText(counts[3])
            self.AddPlateInfo.editControlCount.setText(counts[4])
        except:
            plateInfo = open("PlateInfo.txt", "w")
            plateInfo.write("8,6,12,10,6")
            plateInfo.close()
            plateInfoRead = open("PlateInfo.txt", "r")
            line = str(plateInfoRead.readline())
            counts = line.split(",")
            self.AddPlateInfo.editTopCharCount.setText(counts[0])
            self.AddPlateInfo.editTopMinCharCount.setText(counts[1])
            self.AddPlateInfo.editBottomCharCount.setText(counts[2])
            self.AddPlateInfo.editBottomMinCharCount.setText(counts[3])
            self.AddPlateInfo.editControlCount.setText(counts[4])
        self.AddPlateInfo.exec_()

    def ShowCamerasPage(self):
        self.cameraPage = Cameras()
        self.cameraPage.exec_()

    def ShowAddCameraPage(self):
        self.addCameraPage = AddCamera()
        regexip = QRegExp("[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}")
        regexipaddition = QRegExp("([a-z-A-Z]|[0-9]){1,}.+")
        validatorip = QRegExpValidator(regexip)
        validatoripadittion = QRegExpValidator(regexipaddition)
        self.addCameraPage.editCameraName.setMaxLength(15)
        self.addCameraPage.editCameraIPAddition.setValidator(validatoripadittion)
        self.addCameraPage.editCameraIP.setValidator(validatorip)
        self.addCameraPage.buttonAddCamera.clicked.connect(self.AddCamera)
        self.addCameraPage.exec_()

    def ShowFontsPage(self):
        self.fontsPage = Fonts()
        self.fontsPage.exec_()

    def ShowCharPage(self):
        self.charPage = Char()
        self.charPage.buttonAccept.clicked.connect(self.GetCharInfo)
        self.charPage.editChar.textChanged.connect(self.DisableButton)
        regexchar = QRegExp("[^ a-z]")
        validatorchar = QRegExpValidator(regexchar)
        self.charPage.editChar.setValidator(validatorchar)
        self.charPage.buttonAccept.setEnabled(False)
        self.charPage.exec_()

    def ShowAddFont(self):
        self.addFontPage = AddFont()
        self.addFontPage.buttonAddPhoto.clicked.connect(self.AddFontPhoto)
        self.addFontPage.buttonStartRecording.clicked.connect(self.StartRecording)
        regexwordnumber = QRegExp("\w+\d+")
        validatorwordnumber = QRegExpValidator(regexwordnumber)
        self.addFontPage.buttonStartRecording.setEnabled(False)
        self.addFontPage.editFontName.setValidator(validatorwordnumber)
        self.addFontPage.editFontName.textChanged.connect(self.DisableButtonFontPage)
        self.addFontPage.exec_()

    def SavePlateInfo(self):
        try:
            topCharCount = self.AddPlateInfo.editTopCharCount.text()
            topMinCharCount = self.AddPlateInfo.editTopMinCharCount.text()
            bottomCharCount = self.AddPlateInfo.editBottomCharCount.text()
            bottomMinCharCount = self.AddPlateInfo.editBottomMinCharCount.text()
            controlCount = self.AddPlateInfo.editControlCount.text()
            if (len(topCharCount) != 0 and len(topMinCharCount) != 0 and len(bottomCharCount) != 0 and len(
                    bottomMinCharCount) != 0 and len(controlCount) != 0):
                plateinfo = open("PlateInfo.txt", "w")
                plateinfo.write(
                    topCharCount + "," + topMinCharCount + "," + bottomCharCount + "," + bottomMinCharCount + "," + controlCount)
                plateinfo.close()
                self.AddPlateInfo.close()
            else:
                QMessageBox.warning(self.AddPlateInfo, 'Geçersiz Giriş',
                                    "Lütfen alanları boş bırakmayınız!",
                                    QMessageBox.Ok, QMessageBox.Ok)
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()


    def DisableButtonFontPage(self):
        if (len(self.addFontPage.editFontName.text()) > 0):
            self.addFontPage.buttonStartRecording.setEnabled(True)

    def DisableButton(self):
        if(len(self.charPage.editChar.text())>0):
            self.charPage.buttonAccept.setEnabled(True)

    def AddFontPhoto(self):
        try:
            self.fname, filter = QFileDialog().getOpenFileName(self.addFontPage, 'Font Fotoğrafını Seç', '', ("Image Files (*.jpg)"))
            if self.fname:
                self.LoadPhoto(self.fname)
            else:
                self.fname = None
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()
            self.fname = None
            self.fontPhoto = None
            QMessageBox.warning(self.addFontPage, 'Fotoğraf Uzantı Hatası',
                                "Fotoğraf uzantısını değistirerek tekrar deneyiniz!",
                                QMessageBox.Ok, QMessageBox.Ok)

    def DetectWebcam(self, status):
        try:
            self.trainButton.setEnabled(False)
            self.timerDatabase = QTimer(self)
            if status:
                if (len(self.listCamera) != 0):
                    self.timerDatabase.timeout.connect(self.LoadDatabaseTable)
                    self.timerDatabase.start(1)
                    txtfile = open("ThreadStatus.txt", "w")
                    txtfile.write("True")
                    txtfile.close()
                    for cameraName in self.listCamera:
                        cameraName = DetectPlateThread.camThread(cameraName)
                        cameraName.daemon = True
                        cameraName.start()
                    self.detectButton.setText('Plaka Tanımayı Durdur')
                    self.plateEnabled = True
            else:
                self.timerDatabase.stop()
                txtfile = open("ThreadStatus.txt", "w")
                txtfile.write("False")
                txtfile.close()
                self.detectButton.setText('Plaka Tanimayi Baslat')
                self.trainButton.setEnabled(True)
                self.plateEnabled = False
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def getIP(self):
        try:
            ip = ""
            cameraIP = ""
            topYOne = ""
            topYTwo = ""
            bottomYOne = ""
            bottomYTwo = ""
            cameraName = self.ComboBoxCameras.currentText()
            if (len(cameraName) != 0):
                searchall = curs.execute(
                    """SELECT CameraIP, CameraIPAddition, Username, Password, ProtocolType,
                     TopYOne, TopYTwo, BottomYOne, BottomYTwo FROM Cameras WHERE CameraName = ? """,
                    (cameraName,))
                rows = searchall.fetchall()
                if (rows != None):
                    for row in rows:
                        cameraIP = str(row[0])
                        cameraIPAddition = str(row[1])
                        username = str(row[2])
                        password = str(row[3])
                        protocolType = str(row[4])
                        topYOne = int(row[5])
                        topYTwo = int(row[6])
                        bottomYOne = int(row[7])
                        bottomYTwo = int(row[8])
                    if (username != "" and password != ""):
                        ip = protocolType + "://" + username + ":" + password + "@" + cameraIP + "/" + cameraIPAddition
                    else:
                        ip = protocolType + "://" + cameraIP + "/" + cameraIPAddition
                    return ip, cameraIP, cameraName, topYOne, topYTwo, bottomYOne, bottomYTwo
            else:
                return ip, cameraIP, cameraName, topYOne, topYTwo, bottomYOne, bottomYTwo
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def StartWebcam(self):
        try:
            ip, cameraIP, cameraName, topYOne, topYTwo, bottomYOne, bottomYTwo = self.getIP()
            if (len(cameraName) != 0):
                if (GetPing(cameraIP)):
                    self.cameraStatus = True
                    self.ComboBoxCameras.setEnabled(False)

                    self.StartIPCamera(ip, cameraName, topYOne, topYTwo, bottomYOne, bottomYTwo)
                else:
                    QMessageBox.warning(self, 'Kamera Hatası',
                                        "Kameraya ulaşılamadı. Lütfen kamera bilgilerini kontrol ediniz!\n",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.information(self, 'Kamera Hatası',
                                        "Açılabilecek bir kamera sistemde mevcut değil!\n",
                                        QMessageBox.Ok, QMessageBox.Ok)
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def StartIPCamera(self, ip, cameraName, topYOne, topYTwo, bottomYOne, bottomYTwo):
        try:
            global frameSize
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            curs.execute("DELETE FROM Log")
            conn.commit()
            self.capture = VideoStream(src=ip, resolution=frameSize)
            self.capture.start()
            timercallback = functools.partial(self.UpdateFrame, cameraName=cameraName, topYOne=topYOne, topYTwo=topYTwo,
                                              bottomYOne=bottomYOne, bottomYTwo=bottomYTwo)
            self.timer = QTimer(self)
            self.timer.timeout.connect(timercallback)
            self.timer.start(1)

        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    """def UpdateFrame(self, cameraName, topYOne, topYTwo, bottomYOne, bottomYTwo):
        try:
            while True:
                t.sleep(0.11)
                if (self.cameraStatus == False):
                    break
                self.image = self.capture.read()
                self.image = self.MergeRecAndImage(self.image, topYOne, topYTwo, bottomYOne, bottomYTwo)
                self.DisplayImage(self.image)
                if (cameraName != None and len(cameraName) != 0):
                    self.LoadLogs(cameraName)
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()"""

    def UpdateFrame(self, cameraName, topYOne, topYTwo, bottomYOne, bottomYTwo):
        try:
            if (self.cameraStatus == True):
                self.image = self.capture.read()
                self.image = self.MergeRecAndImage(self.image, topYOne, topYTwo, bottomYOne, bottomYTwo)
                self.DisplayImage(self.image)
                if (cameraName != None and len(cameraName) != 0):
                    self.LoadLogs(cameraName)
            else:
                self.DisplayImage(self.backimage)
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def MergeRecAndImage(self,image,topYOne, topYTwo, bottomYOne, bottomYTwo):
        try:
            cv2.rectangle(image, (0, int(topYOne)), (640, int(topYTwo)), (255, 0, 0), 2)
            cv2.rectangle(image, (0, int(bottomYOne)), (640, int(bottomYTwo)), (0, 0, 255), 2)
            return image
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def StopWebcam(self):
        try:
            self.cameraStatus = False
            self.timer.stop()
            self.DisplayImage(self.backimage)
            self.ComboBoxCameras.setEnabled(True)
            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(False)
        except:
            print("hata stopwebcamde")

    def TrainPlates(self):
        blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # KNN eğitimi
        if blnKNNTrainingSuccessful == False:  # Eğer KNN eğitimi başarılı değilse
            QMessageBox.warning(self, 'KNN Taraması',
                                "KNN dosya taraması yapılamadı!\n",
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.plateTrain = True
            self.detectButton.setEnabled(True)
            QMessageBox.information(self, 'KNN Taraması',
                                    "KNN dosyası başarıyla tarandı!\n",
                                    QMessageBox.Ok, QMessageBox.Ok)

    def StartRecording(self):
        try:
            MIN_CONTOUR_AREA = 100
            RESIZED_WIDTH_FOR_GUI = 310
            RESIZED_HEIGHT_FOR_GUI = 260
            RESIZED_IMAGE_WIDTH = 20
            RESIZED_IMAGE_HEIGHT = 30
            Check = True
            if (len(str(self.addFontPage.editFontName.text())) != 0):
                if (self.fname != None):
                    fontName = str(self.addFontPage.editFontName.text())
                    stream = open(self.fname, "rb")
                    bytes = bytearray(stream.read())
                    numpyarray = np.asarray(bytes, dtype=np.uint8)
                    imgTrainingNumbers = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
                    imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)
                    imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)
                    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                      cv2.THRESH_BINARY_INV, 11, 2)
                    imgThreshCopy = imgThresh.copy()
                    npaContours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_EXTERNAL,
                                                                 cv2.CHAIN_APPROX_SIMPLE)
                    npaFlattenedImages = np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
                    charCount = 0
                    intClassifications = []
                    intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'),
                                     ord('8'),
                                     ord('9'), ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'),
                                     ord('H'),
                                     ord('I'), ord('J'), ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'),
                                     ord('Q'),
                                     ord('R'), ord('S'), ord('T'), ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'),
                                     ord('Z'),
                                     ord('/'), ord('-'), ord('@')]
                    for npaContour in npaContours:  # for each contour
                        if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:
                            [intX, intY, intW, intH] = cv2.boundingRect(npaContour)
                            imgCharCropped = imgTrainingNumbers[intY + 1:intY + intH, intX + 1:intX + intW]
                            cv2.rectangle(imgTrainingNumbers, (intX, intY), (intX + intW, intY + intH), (0, 0, 255), 1)
                            imgROI = imgThresh[intY:intY + intH, intX:intX + intW]
                            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
                            imgThreshCharCroppedResized = cv2.resize(imgROI,
                                                                     (RESIZED_WIDTH_FOR_GUI, RESIZED_HEIGHT_FOR_GUI))
                            imgCharCroppedResized = cv2.resize(imgCharCropped,
                                                               (RESIZED_WIDTH_FOR_GUI, RESIZED_HEIGHT_FOR_GUI))
                            self.DisplayPhoto(imgCharCroppedResized, "Char")
                            self.DisplayPhoto(imgThreshCharCroppedResized, "Thresh")
                            self.DisplayPhoto(imgTrainingNumbers, "Font")
                            self.ShowCharPage()
                            intChar = self.char
                            if intChar == None:  # ESC
                                Check = False
                                QMessageBox.warning(self.addFontPage, 'Çıkış',
                                                    "İşlem iptal edildi!",
                                                    QMessageBox.Ok, QMessageBox.Ok)
                                self.addFontPage.close()
                            if intChar in intValidChars:
                                intClassifications.append(intChar)
                                npaFlattenedImage = imgROIResized.reshape(
                                    (1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
                                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)
                                charCount = charCount + 1
                                self.char = None
                        if (Check == False):
                            break
                    fltClassifications = np.array(intClassifications, np.float32)
                    npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))
                    if (Check == True):
                        if (len(fontName) > 0):
                            search = curs.execute('SELECT FontName FROM Fonts WHERE FontName = ? ', (fontName,))
                            results = search.fetchone()
                            if (results == None):
                                newpath = path + "Fonts" + "\\" + str(fontName) + "\\"
                                an = datetime.datetime.now()
                                fontDate = str(an.day) + "/" + str(an.month) + "/" + str(an.year)
                                curs.execute("""INSERT INTO Fonts(FontName, FontDate, FontFileDir, CharCountInFont) 
                                                            VALUES(?,?,?,?)""",
                                             (fontName, str(fontDate), newpath, str(charCount)))
                                conn.commit()
                                charCount = 0
                                os.makedirs(newpath)
                                np.savetxt(newpath + "classifications.txt",
                                           npaClassifications)  # write flattened images to file
                                np.savetxt(newpath + "flattened_images.txt", npaFlattenedImages)  #
                                self.char == None
                                self.addFontPage.close()
                                QMessageBox.information(self.addFontPage, 'Kayıt Başarılı',
                                                        "Font için sınıflandırma ve fotoğraf dizeleri başarıyla oluşturuldu!",
                                                        QMessageBox.Ok, QMessageBox.Ok)
                else:
                    QMessageBox.warning(self.addFontPage, 'Geçersiz İşlem',
                                        "Lütfen font için bir fotoğraf seçiniz!",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self.addFontPage, 'Font İsim Hatası',
                                    "Lütfen font için isim giriniz!",
                                    QMessageBox.Ok, QMessageBox.Ok)

        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def GetCharInfo(self):
        char = self.charPage.editChar.text()
        if (char != ""):
            self.char = ord(char)
            self.char = int(self.char)
            self.charPage.close()
        else:
            self.charPage.close()
            self.addFontPage.close()
            QMessageBox.warning(self.addFontPage, 'Harf Hatası',
                                "Lütfen tekrar deneyiniz!",
                                QMessageBox.Ok, QMessageBox.Ok)

    def LoadPhoto(self, fname):
        try:
            stream = open(fname, "rb")
            bytes = bytearray(stream.read())
            numpyarray = np.asarray(bytes, dtype=np.uint8)
            self.fontPhoto = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
            self.DisplayPhoto(self.fontPhoto, "Font")
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()
    def CountofLetter(self,text,let):
        count = 0
        for letter in text:
            if letter == let:
                count = count + 1
        return count

    def AddCamera(self):
        try:
            cameraName = self.addCameraPage.editCameraName.text()
            cameraIP = self.addCameraPage.editCameraIP.text()
            cameraIPAddition = self.addCameraPage.editCameraIPAddition.text()
            username = self.addCameraPage.editUsername.text()
            password = self.addCameraPage.editPassword.text()
            protocolType = "rtsp"
            location = self.addCameraPage.editLocation.toPlainText()
            minPixelWidth = Database.MIN_PIXEL_WIDTH
            minPixelHeight = Database.MIN_PIXEL_HEIGHT
            minPixelArea = Database.MIN_PIXEL_AREA
            minPixelRatio = Database.MIN_ASPECT_RATIO
            maxPixelRatio = Database.MAX_ASPECT_RATIO
            minDiagSize = Database.MIN_DIAG_SIZE_MULTIPLE_AWAY
            maxDiagSize = Database.MAX_DIAG_SIZE_MULTIPLE_AWAY
            maxChangeInArea = Database.MAX_CHANGE_IN_AREA
            maxChangeInWidth = Database.MAX_CHANGE_IN_WIDTH
            maxChangeInHeight = Database.MAX_CHANGE_IN_HEIGHT
            maxAngleBetweenChar = Database.MAX_ANGLE_BETWEEN_CHARS
            minNumberOfMatchCharNumber = Database.MIN_NUMBER_OF_MATCHING_CHARS
            cameraStatus = "Çalışmıyor"
            topYOne = 0
            topYTwo = 240
            bottomYOne = 240
            bottomYTwo = 480
            countDot = self.CountofLetter(cameraIP, ".")
            search = curs.execute('SELECT CameraName FROM Cameras WHERE CameraName = ? ', (cameraName,))
            results = search.fetchone()
            if (len(cameraIP) < 16 and len(cameraIP) > 6 and len(cameraName) != 0 and countDot == 3):
                if (cameraIP[-1] == "."):
                    cameraIP = cameraIP + "0"
                if (results == None):
                    if (self.addCameraPage.radioButtonRtsp.isChecked() == True):
                        protocolType = "rtsp"
                    if (self.addCameraPage.radioButtonHttp.isChecked() == True):
                        protocolType = "http"
                    if (len(location) != 0):
                        curs.execute("""INSERT INTO Cameras(CameraName,CameraIP,CameraIPAddition,Username,Password, 
                                                ProtocolType, MinPixelWidth ,MinPixelHeight,MinPixelArea,MinPixelRatio,MaxPixelRatio,MinDiagSize,
                                                MaxDiagSize,MaxChangeInArea,MaxChangeInWidth,MaxChangeInHeight,MaxAngleBetweenChar,MinNumberOfMatchCharNumber,
                                                TopYOne,TopYTwo,BottomYOne,BottomYTwo,CameraStatus, CameraLocation) 
                                                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                            cameraName, cameraIP, cameraIPAddition, username, password, protocolType, minPixelWidth,
                            minPixelHeight,
                            minPixelArea, minPixelRatio, maxPixelRatio, minDiagSize, maxDiagSize, maxChangeInArea,
                            maxChangeInWidth,
                            maxChangeInHeight, maxAngleBetweenChar, minNumberOfMatchCharNumber, topYOne, topYTwo,
                            bottomYOne,
                            bottomYTwo, cameraStatus, location))
                        conn.commit()
                        protocolType = "rtsp"
                        self.addCameraPage.close()
                        QMessageBox.information(self.addCameraPage, 'Kayıt Başarılı',
                                                "Kamera sisteme eklendi!\n",
                                                QMessageBox.Ok, QMessageBox.Ok)
                    else:
                        QMessageBox.warning(self.addCameraPage, 'Geçersiz Konum!',
                                            "Lütfen kamera konumunu giriniz!\n",
                                            QMessageBox.Ok, QMessageBox.Ok)
                else:
                    QMessageBox.warning(self.addCameraPage, 'Geçersiz Kamera İsmi!',
                                        "Eklenmek istenen kamera adı sistemde mevcut!\n",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self.addCameraPage, 'Geçersiz Bilgi!',
                                    "Eklenmek istenen bilgileri kontrol ediniz!\n",
                                    QMessageBox.Ok, QMessageBox.Ok)
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def LoadDatabase(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        while True:
            res = conn.execute('SELECT Plate,Date,Time,Camera FROM Plates')
            for row_index, row_data in enumerate(res):
                self.tableWidget.insertRow(row_index)
                for colm_index, colm_data in enumerate(row_data):
                    self.tableWidget.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
            return

    def LoadLogs(self, cameraName):
        while self.tableWidget_2.rowCount() > 0:
            self.tableWidget_2.removeRow(0)
        res = conn.execute('SELECT Plate,Date,Time FROM Log WHERE Camera = ?', (cameraName,))
        for row_index, row_data in enumerate(res):
            self.tableWidget_2.insertRow(row_index)
            for colm_index, colm_data in enumerate(row_data):
                self.tableWidget_2.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
        return

    def DisplayImage(self, img):
        try:
            qformat = QImage.Format_Indexed8
            if len(img.shape) == 3:  # [0]=satırlar, [1]=sütunlar, [2]=kanallar
                if img.shape[2] == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888
            outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
            outImage = outImage.rgbSwapped()
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
        except:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def DisplayPhoto(self, img,type):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        if (str(type) == "Font"):
            self.addFontPage.labelFontPhoto.setPixmap(QPixmap.fromImage(outImage))
            self.addFontPage.labelFontPhoto.setScaledContents(True)
        if(str(type)=="Char"):
            self.addFontPage.labelOriginalCroppedChar.setPixmap(QPixmap.fromImage(outImage))
            self.addFontPage.labelOriginalCroppedChar.setScaledContents(True)
        if (str(type) == "Thresh"):
            self.addFontPage.labelThreshCroppedChar.setPixmap(QPixmap.fromImage(outImage))
            self.addFontPage.labelThreshCroppedChar.setScaledContents(True)

##############################################################################################
class Cameras(QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        super(Cameras,self).__init__(parent)
        self.setupUi(self)
        try:
            self.setWindowIcon(QIcon(str(path) + "\\vagonplaka.png"))
        except Exception:
            pass
        self.setWindowTitle('Kameralar')
        self.LoadCameraDatabase()
        self.InitUi()
        self.topYone= 0
        self.topYtwo= 240
        self.bottomYone = 240
        self.bottomYtwo = 480
        try:
            self.backimage= cv2.imread(path + 'Fonts\\background.png')
        except:
            pass
        self.bottomYtwo =480
        self.oldCameraName = None

    def InitUi(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.buttonAddCamera.clicked.connect(self.ShowAddCameraPage)
        self.buttonUpdateCamera.clicked.connect(self.ShowUpdateCameraPage)
        self.buttonDeleteCamera.clicked.connect(self.DeleteCamera)
        self.tableWidget.itemClicked.connect(self.TableClicked)
        self.buttonUpdateCamera.setEnabled(False)
        self.buttonDeleteCamera.setEnabled(False)

    def ShowUpdateCameraPage(self):
        self.updateCameraPage = UpdateCamera()
        self.buttonUpdateCamera.setEnabled(False)
        self.buttonDeleteCamera.setEnabled(False)
        self.updateCameraPage.buttonShowContours.clicked.connect(self.Contours)
        self.updateCameraPage.buttonSaveConfiguration.clicked.connect(self.UpdateCamera)
        regexint = QRegExp("[0-9_]+")
        regexip = QRegExp("[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}")
        regexfloat = QRegExp("[0-9]{1,3}\\.[0-9]{1,2}")
        validatorint = QRegExpValidator(regexint)
        validatorip = QRegExpValidator(regexip)
        validatorfloat = QRegExpValidator(regexfloat)
        self.updateCameraPage.editCameraIP.setValidator(validatorip)
        self.updateCameraPage.editTopY1.setValidator(validatorint)
        self.updateCameraPage.editTopY2.setValidator(validatorint)
        self.updateCameraPage.editBottomY1.setValidator(validatorint)
        self.updateCameraPage.editBottomY2.setValidator(validatorint)
        self.updateCameraPage.editMinPixelWidth.setValidator(validatorint)
        self.updateCameraPage.editMinPixelHeight.setValidator(validatorint)
        self.updateCameraPage.editMinPixelArea.setValidator(validatorint)
        self.updateCameraPage.editMinNumberOfMatchCharNumber.setValidator(validatorint)
        self.updateCameraPage.editMinPixelRatio.setValidator(validatorfloat)
        self.updateCameraPage.editMaxPixelRatio.setValidator(validatorfloat)
        self.updateCameraPage.editMinDiagSize.setValidator(validatorfloat)
        self.updateCameraPage.editMaxDiagSize.setValidator(validatorfloat)
        self.updateCameraPage.editMaxChangeInArea.setValidator(validatorfloat)
        self.updateCameraPage.editMaxChangeInWidth.setValidator(validatorfloat)
        self.updateCameraPage.editMaxChangeInHeight.setValidator(validatorfloat)
        self.updateCameraPage.editMaxAngleBetweenChar.setValidator(validatorfloat)
        self.updateCameraPage.editTopY1.setMaxLength(4)
        self.updateCameraPage.editTopY2.setMaxLength(4)
        self.updateCameraPage.editBottomY1.setMaxLength(4)
        self.updateCameraPage.editBottomY2.setMaxLength(4)
        self.ShowCameraData()
        self.updateCameraPage.exec_()

    def ShowAddCameraPage(self):
        self.addCameraPage = AddCamera()
        self.addCameraPage.buttonAddCamera.clicked.connect(self.AddCamera)

        regexip = QRegExp("[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}")
        regexipaddition = QRegExp("([a-z-A-Z]|[0-9]){1,}.+")
        validatorip = QRegExpValidator(regexip)
        validatoripadittion = QRegExpValidator(regexipaddition)
        self.addCameraPage.editCameraName.setMaxLength(15)
        self.addCameraPage.editCameraIPAddition.setValidator(validatoripadittion)
        self.addCameraPage.editCameraIP.setValidator(validatorip)
        self.addCameraPage.exec_()

    def CountofLetter(self,text,let):
        count = 0
        for letter in text:
            if letter == let:
                count = count + 1
        return count

    def AddCamera(self):
        try:
            cameraName = self.addCameraPage.editCameraName.text()
            cameraIP = self.addCameraPage.editCameraIP.text()
            cameraIPAddition = self.addCameraPage.editCameraIPAddition.text()
            username = self.addCameraPage.editUsername.text()
            password = self.addCameraPage.editPassword.text()
            protocolType = "rtsp"
            location = self.addCameraPage.editLocation.toPlainText()
            minPixelWidth = Database.MIN_PIXEL_WIDTH
            minPixelHeight = Database.MIN_PIXEL_HEIGHT
            minPixelArea = Database.MIN_PIXEL_AREA
            minPixelRatio = Database.MIN_ASPECT_RATIO
            maxPixelRatio = Database.MAX_ASPECT_RATIO
            minDiagSize = Database.MIN_DIAG_SIZE_MULTIPLE_AWAY
            maxDiagSize = Database.MAX_DIAG_SIZE_MULTIPLE_AWAY
            maxChangeInArea = Database.MAX_CHANGE_IN_AREA
            maxChangeInWidth = Database.MAX_CHANGE_IN_WIDTH
            maxChangeInHeight = Database.MAX_CHANGE_IN_HEIGHT
            maxAngleBetweenChar = Database.MAX_ANGLE_BETWEEN_CHARS
            minNumberOfMatchCharNumber = Database.MIN_NUMBER_OF_MATCHING_CHARS
            cameraStatus = "Çalışmıyor"
            topYOne = 0
            topYTwo = 240
            bottomYOne = 240
            bottomYTwo = 480
            countDot = self.CountofLetter(cameraIP, ".")
            search = curs.execute('SELECT CameraName FROM Cameras WHERE CameraName = ? ', (cameraName,))
            results = search.fetchone()
            if (len(cameraIP) < 16 and len(cameraIP) > 6 and len(cameraName) != 0 and countDot == 3):
                if (cameraIP[-1] == "."):
                    cameraIP = cameraIP + "0"
                if (results == None):
                    if (self.addCameraPage.radioButtonRtsp.isChecked() == True):
                        protocolType = "rtsp"
                    if (self.addCameraPage.radioButtonHttp.isChecked() == True):
                        protocolType = "http"
                    if (len(location) != 0):
                        curs.execute("""INSERT INTO Cameras(CameraName,CameraIP,CameraIPAddition,Username,Password, 
                                                ProtocolType, MinPixelWidth ,MinPixelHeight,MinPixelArea,MinPixelRatio,MaxPixelRatio,MinDiagSize,
                                                MaxDiagSize,MaxChangeInArea,MaxChangeInWidth,MaxChangeInHeight,MaxAngleBetweenChar,MinNumberOfMatchCharNumber,
                                                TopYOne,TopYTwo,BottomYOne,BottomYTwo,CameraStatus, CameraLocation) 
                                                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                            cameraName, cameraIP, cameraIPAddition, username, password, protocolType, minPixelWidth,
                            minPixelHeight,
                            minPixelArea, minPixelRatio, maxPixelRatio, minDiagSize, maxDiagSize, maxChangeInArea,
                            maxChangeInWidth,
                            maxChangeInHeight, maxAngleBetweenChar, minNumberOfMatchCharNumber, topYOne, topYTwo,
                            bottomYOne,
                            bottomYTwo, cameraStatus, location))
                        conn.commit()
                        protocolType = "rtsp"
                        self.addCameraPage.close()
                        QMessageBox.information(self.addCameraPage, 'Kayıt Başarılı',
                                                "Kamera sisteme eklendi!\n",
                                                QMessageBox.Ok, QMessageBox.Ok)
                    else:
                        QMessageBox.warning(self.addCameraPage, 'Geçersiz Konum!',
                                            "Lütfen kamera konumunu giriniz!\n",
                                            QMessageBox.Ok, QMessageBox.Ok)
                else:
                    QMessageBox.warning(self.addCameraPage, 'Geçersiz Kamera İsmi!',
                                        "Eklenmek istenen kamera adı sistemde mevcut!\n",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self.addCameraPage, 'Geçersiz Bilgi!',
                                    "Eklenmek istenen bilgileri kontrol ediniz!\n",
                                    QMessageBox.Ok, QMessageBox.Ok)
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def ContourSize(self,topYOne,topYTwo,bottomYOne,bottomYTwo):
        if (int(topYOne) < 0):
            topYOne = 0
        if (int(topYOne) > 480):
            topYOne = 480
        if (int(topYTwo) < 0):
            topYTwo = 0
        if (int(topYTwo) > 480):
            topYTwo = 480
        if (int(bottomYOne) < 0):
            bottomYOne = 0
        if (int(bottomYOne) > 480):
            bottomYOne = 480
        if (int(bottomYTwo) < 0):
            bottomYTwo = 0
        if (int(bottomYTwo) > 480):
            bottomYTwo = 480
        return topYOne,topYTwo,bottomYOne,bottomYTwo

    def Contours(self):
        try:
            cameraIP = self.updateCameraPage.editCameraIP.text()
            cameraIPAddition = self.updateCameraPage.editCameraIPAddition.text()
            username = self.updateCameraPage.editUsername.text()
            password = self.updateCameraPage.editPassword.text()
            topYOne = self.updateCameraPage.editTopY1.text()
            topYTwo = self.updateCameraPage.editTopY2.text()
            bottomYOne = self.updateCameraPage.editBottomY1.text()
            bottomYTwo = self.updateCameraPage.editBottomY2.text()
            protocolType = "rtsp"
            if (self.updateCameraPage.radioButtonRtsp.isChecked() == True):
                protocolType = "rtsp"
            if (self.updateCameraPage.radioButtonHttp.isChecked() == True):
                protocolType = "http"
            if (username != "" and password != ""):
                ip = str(protocolType) + "://" + str(username) + ":" + str(password) + "@" + str(
                    cameraIP) + "/" + cameraIPAddition
            else:
                ip = str(protocolType) + "://" + str(cameraIP) + "/" + cameraIPAddition

            if (len(topYOne) != 0 and len(topYTwo) != 0 and len(bottomYOne) != 0 and len(bottomYTwo) != 0):
                if(topYOne!=topYTwo and bottomYOne!=bottomYTwo):
                    topYOne, topYTwo, bottomYOne, bottomYTwo = self.ContourSize(topYOne, topYTwo, bottomYOne,
                                                                                bottomYTwo)
                    self.GetFrameFromCamera(cameraIP, ip, topYOne, topYTwo, bottomYOne, bottomYTwo)
                else:
                    QMessageBox.warning(self.updateCameraPage, 'Hatalı Giriş',
                                        "Bölümlerde üst ve alt sınır aynı olamaz!" + "\n",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self.updateCameraPage, 'Hatalı Giriş',
                                    "Girilen değerler 0-480 arasında olmak zorundadır!" + "\n",
                                    QMessageBox.Ok, QMessageBox.Ok)
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def GetFrameFromCamera(self, cameraIP, ip, topYOne, topYTwo, bottomYOne, bottomYTwo):
        try:
            global frameSize
            if (GetPing(cameraIP)):
                captureforsc = VideoStream(src=str(ip), resolution=frameSize)
                captureforsc.start()
                screenshot = captureforsc.read()
                #captureforsc.stream.stream.release()
                if (str(screenshot) != "None"):
                    img = self.ShowContours(screenshot, topYOne, topYTwo, bottomYOne, bottomYTwo)
                    self.DisplayPhoto(img)
                    screenshot = None
                else:
                    self.DisplayPhoto(self.backimage)
                    self.updateCameraPage.buttonShowContours.setEnabled(False)
                    QMessageBox.warning(self.updateCameraPage, 'Kamera Hatası!',
                                        "Ulaşılmak istenen kameraya erişim sağlanamadı. Lütfen bilgileri kontrol ediniz!\n" + "IP: " + ip + "\n",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                self.DisplayPhoto(self.backimage)
                self.updateCameraPage.buttonShowContours.setEnabled(False)
                QMessageBox.warning(self.updateCameraPage, 'Kamera Hatası!',
                                    "Ulaşılmak istenen kameraya erişim sağlanamadı. Lütfen bilgileri kontrol ediniz!\n" + "IP: " + ip + "\n",
                                    QMessageBox.Ok, QMessageBox.Ok)
        except:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def ShowContours(self,img,topyone,topytwo,bottomyone,bottomytwo):
        try:
            cv2.rectangle(img, (0, int(topyone)), (640, int(topytwo)), (255, 0, 0), 2)
            cv2.rectangle(img, (0, int(bottomyone)), (640, int(bottomytwo)), (0, 0, 255), 2)
            return img
        except:
            return img

    def ShowCameraData(self):
        try:
            content = 'SELECT * FROM Cameras'
            res = conn.execute(content)
            for row in enumerate(res):
                if row[0] == self.tableWidget.currentRow():
                    data = row[1]
                    self.oldCameraName = data[1]
                    cameraName = self.oldCameraName
                    cameraIP = data[2]
                    cameraIPAddition = data[3]
                    username = data[4]
                    password = data[5]
                    protocolType = data[6]
                    minPixelWidth = data[7]
                    minPixelHeight = data[8]
                    minPixelArea = data[9]
                    minPixelRatio = data[10]
                    maxPixelRatio = data[11]
                    minDiagSize = data[12]
                    maxDiagSize = data[13]
                    maxChangeInArea = data[14]
                    maxChangeInWidth = data[15]
                    maxChangeInHeight = data[16]
                    maxAngleBetweenChar = data[17]
                    minNumberOfMatchCharNumber = data[18]
                    topYOne = data[19]
                    topYTwo = data[20]
                    bottomYOne = data[21]
                    bottomYTwo = data[22]
                    cameraStatus = data[23]
                    location = data[24]
                    self.updateCameraPage.editCameraName.setText(str(cameraName))
                    self.updateCameraPage.editCameraIP.setText(str(cameraIP))
                    self.updateCameraPage.editCameraIPAddition.setText(str(cameraIPAddition))
                    self.updateCameraPage.editUsername.setText(str(username))
                    self.updateCameraPage.editPassword.setText(str(password))
                    self.updateCameraPage.editLocation.setText(str(location))
                    self.updateCameraPage.editMinPixelWidth.setText(str(minPixelWidth))
                    self.updateCameraPage.editMinPixelHeight.setText(str(minPixelHeight))
                    self.updateCameraPage.editMinPixelArea.setText(str(minPixelArea))
                    self.updateCameraPage.editMinPixelRatio.setText(str(minPixelRatio))
                    self.updateCameraPage.editMaxPixelRatio.setText(str(maxPixelRatio))
                    self.updateCameraPage.editMinDiagSize.setText(str(minDiagSize))
                    self.updateCameraPage.editMaxDiagSize.setText(str(maxDiagSize))
                    self.updateCameraPage.editMaxChangeInArea.setText(str(maxChangeInArea))
                    self.updateCameraPage.editMaxChangeInWidth.setText(str(maxChangeInWidth))
                    self.updateCameraPage.editMaxChangeInHeight.setText(str(maxChangeInHeight))
                    self.updateCameraPage.editMaxAngleBetweenChar.setText(str(maxAngleBetweenChar))
                    self.updateCameraPage.editMinNumberOfMatchCharNumber.setText(str(minNumberOfMatchCharNumber))
                    self.updateCameraPage.editTopY1.setText(str(topYOne))
                    self.updateCameraPage.editTopY2.setText(str(topYTwo))
                    self.updateCameraPage.editBottomY1.setText(str(bottomYOne))
                    self.updateCameraPage.editBottomY2.setText(str(bottomYTwo))
                    if (username != "" and password != ""):
                        ip = str(protocolType) + "://" + str(username) + ":" + str(password) + "@" + str(
                            cameraIP) + "/" + cameraIPAddition
                    else:
                        ip = str(protocolType) + "://" + str(cameraIP) + "/" + cameraIPAddition
                    if (protocolType == "rtsp"):
                        self.updateCameraPage.radioButtonRtsp.setChecked(True)
                    if (protocolType == "http"):
                        self.updateCameraPage.radioButtonHttp.setChecked(True)
                    if (cameraStatus == "Çalışıyor"):
                        self.updateCameraPage.radioButtonWorking.setChecked(True)
                        self.GetFrameFromCamera(cameraIP, ip, topYOne, topYTwo, bottomYOne, bottomYTwo)
                    if (cameraStatus == "Çalışmıyor"):
                        self.updateCameraPage.radioButtonNotWorking.setChecked(True)
                        self.updateCameraPage.buttonShowContours.setEnabled(False)
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def UpdateCamera(self):
        try:
            countDot = 0
            cameraName = self.updateCameraPage.editCameraName.text()
            cameraIP = self.updateCameraPage.editCameraIP.text()
            cameraIPAddition = self.updateCameraPage.editCameraIPAddition.text()
            username = self.updateCameraPage.editUsername.text()
            password = self.updateCameraPage.editPassword.text()
            location = self.updateCameraPage.editLocation.text()
            minPixelWidth = self.updateCameraPage.editMinPixelWidth.text()
            minPixelHeight = self.updateCameraPage.editMinPixelHeight.text()
            minPixelArea = self.updateCameraPage.editMinPixelArea.text()
            minPixelRatio = self.updateCameraPage.editMinPixelRatio.text()
            maxPixelRatio = self.updateCameraPage.editMaxPixelRatio.text()
            minDiagSize = self.updateCameraPage.editMinDiagSize.text()
            maxDiagSize = self.updateCameraPage.editMaxDiagSize.text()
            maxChangeInArea = self.updateCameraPage.editMaxChangeInArea.text()
            maxChangeInWidth = self.updateCameraPage.editMaxChangeInWidth.text()
            maxChangeInHeight = self.updateCameraPage.editMaxChangeInHeight.text()
            maxAngleBetweenChar = self.updateCameraPage.editMaxAngleBetweenChar.text()
            minNumberOfMatchCharNumber = self.updateCameraPage.editMinNumberOfMatchCharNumber.text()
            topYOne = self.updateCameraPage.editTopY1.text()
            topYTwo = self.updateCameraPage.editTopY2.text()
            bottomYOne = self.updateCameraPage.editBottomY1.text()
            bottomYTwo = self.updateCameraPage.editBottomY2.text()
            if (len(topYOne) != 0 and len(topYTwo) != 0 and len(bottomYOne) != 0 and len(bottomYTwo) != 0 and topYOne!=topYTwo and bottomYOne!=bottomYTwo):
                topYOne, topYTwo, bottomYOne, bottomYTwo = self.ContourSize(topYOne, topYTwo, bottomYOne, bottomYTwo)
                protocolType = "rtsp"
                cameraStatus = "Çalışmıyor"
                if (self.updateCameraPage.radioButtonRtsp.isChecked() == True):
                    protocolType = "rtsp"
                if (self.updateCameraPage.radioButtonHttp.isChecked() == True):
                    protocolType = "http"
                if (self.updateCameraPage.radioButtonWorking.isChecked() == True):
                    cameraStatus = "Çalışıyor"
                if (self.updateCameraPage.radioButtonNotWorking.isChecked() == True):
                    cameraStatus = "Çalışmıyor"
                if (len(cameraIP) < 16 and len(cameraIP) > 6):
                    countDot = self.CountofLetter(cameraIP, ".")
                search = curs.execute('SELECT CameraName FROM Cameras')
                check = True
                rows = search.fetchall()
                for row in rows:
                    if (str(row[0]).lower() == cameraName.lower()):
                        check = False
                if (len(minPixelWidth) != 0 and len(minPixelHeight) != 0 and len(minPixelArea) != 0
                        and len(minPixelRatio) != 0 and len(minDiagSize) != 0 and len(maxDiagSize) != 0
                        and len(maxChangeInArea) != 0 and len(maxChangeInWidth) != 0 and len(maxChangeInHeight) != 0
                        and len(maxAngleBetweenChar) != 0 and len(minNumberOfMatchCharNumber) != 0 and countDot == 3
                        and len(cameraName) != 0 and len(location)!= 0):
                    minPixelRatio = str(float(minPixelRatio))
                    maxPixelRatio = str(float(maxPixelRatio))
                    minDiagSize = str(float(minDiagSize))
                    maxDiagSize = str(float(maxDiagSize))
                    maxChangeInArea = str(float(maxChangeInArea))
                    maxChangeInWidth = str(float(maxChangeInWidth))
                    maxChangeInHeight = str(float(maxChangeInHeight))
                    maxAngleBetweenChar = str(float(maxAngleBetweenChar))
                    if (cameraIP[-1] == "."):
                        cameraIP = cameraIP + "0"
                    if (str(self.oldCameraName) == cameraName):
                        curs.execute("""UPDATE Cameras SET CameraName = ? , CameraIP = ? , CameraIPAddition = ? , Username = ? , Password = ? , 
                                                    ProtocolType = ? , MinPixelWidth = ? , MinPixelHeight = ? , MinPixelArea = ? , MinPixelRatio = ? , 
                                                    MaxPixelRatio = ? , MinDiagSize = ? , MaxDiagSize = ? , MaxChangeInArea = ? , MaxChangeInWidth = ? , 
                                                    MaxChangeInHeight = ? , MaxAngleBetweenChar = ? , MinNumberOfMatchCharNumber = ? , TopYOne = ? , 
                                                    TopYTwo = ? , BottomYOne = ? , BottomYTwo = ? , CameraStatus = ?, CameraLocation = ? WHERE CameraName = ?""",
                                     (cameraName, cameraIP, cameraIPAddition, username, password, protocolType,
                                      minPixelWidth,
                                      minPixelHeight, minPixelArea, minPixelRatio, maxPixelRatio, minDiagSize,
                                      maxDiagSize,
                                      maxChangeInArea, maxChangeInWidth, maxChangeInHeight, maxAngleBetweenChar,
                                      minNumberOfMatchCharNumber, topYOne, topYTwo, bottomYOne, bottomYTwo,
                                      cameraStatus, location, self.oldCameraName))
                        conn.commit()
                        self.LoadCameraDatabase()
                        QMessageBox.information(self.updateCameraPage, 'Güncelleme Başarılı',
                                                "Kamera konfigürasyon güncellemesi başarı ile yapıldı!",
                                                QMessageBox.Ok, QMessageBox.Ok)
                        self.updateCameraPage.close()

                    else:
                        if (check == True):
                            curs.execute("""UPDATE Cameras SET CameraName = ? , CameraIP = ? , CameraIPAddition = ? , 
                                                    Username = ? , Password = ? , ProtocolType = ? , MinPixelWidth = ? , MinPixelHeight = ? , 
                                                    MinPixelArea = ? , MinPixelRatio = ? , MaxPixelRatio = ? , MinDiagSize = ? , MaxDiagSize = ? , 
                                                    MaxChangeInArea = ? , MaxChangeInWidth = ? , MaxChangeInHeight = ? , MaxAngleBetweenChar = ? , 
                                                    MinNumberOfMatchCharNumber = ? , TopYOne = ? , TopYTwo = ? , BottomYOne = ? , BottomYTwo = ?, 
                                                    CameraStatus = ? , CameraLocation = ? WHERE CameraName = ?""",
                                         (cameraName, cameraIP, cameraIPAddition, username, password, protocolType,
                                          minPixelWidth,
                                          minPixelHeight, minPixelArea, minPixelRatio, maxPixelRatio, minDiagSize,
                                          maxDiagSize,
                                          maxChangeInArea, maxChangeInWidth, maxChangeInHeight, maxAngleBetweenChar,
                                          minNumberOfMatchCharNumber, topYOne, topYTwo, bottomYOne, bottomYTwo,
                                          cameraStatus, location, self.oldCameraName))
                            conn.commit()
                            self.LoadCameraDatabase()
                            QMessageBox.information(self.updateCameraPage, 'Güncelleme Başarılı',
                                                    "Kamera konfigürasyon güncellemesi başarı ile yapıldı!\n",
                                                    QMessageBox.Ok, QMessageBox.Ok)
                            self.updateCameraPage.close()
                        else:
                            QMessageBox.warning(self.updateCameraPage, 'Güncelleme Hatası',
                                                "Girilen kamera ismi sistemde mevcut!\n",
                                                QMessageBox.Ok, QMessageBox.Ok)
                else:
                    QMessageBox.warning(self.updateCameraPage, 'Güncelleme Hatası',
                                        "Girilen bilgiler geçersiz!\n",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self.updateCameraPage, 'Fotoğraf Kontürleri',
                                    "Lütfen fotoğraf kontürleri (üst ve alt sınırlar) için geçerli değerler giriniz!\n",
                                    QMessageBox.Ok, QMessageBox.Ok)
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()


    def DisplayPhoto(self, img):
        try:
            qformat = QImage.Format_Indexed8
            if len(img.shape) == 3:  # rows[0],cols[1],channels[2]
                if (img.shape[2]) == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888
            img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
            # BGR >RGB
            img = img.rgbSwapped()
            self.updateCameraPage.labelCalibrationPhoto.setPixmap(QPixmap.fromImage(img))
            self.updateCameraPage.labelCalibrationPhoto.setScaledContents(True)
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(f) + "\n")
            logToday.close()

    def DeleteCamera(self):
        try:
            self.buttonDeleteCamera.setEnabled(False)
            self.buttonUpdateCamera.setEnabled(False)
            content = "SELECT * FROM Cameras"
            res = conn.execute(content)
            for row in enumerate(res):
                if row[0] == self.tableWidget.currentRow():
                    data = row[1]
                    cameraName = data[1]
                    buttonReply = QMessageBox.question(self, 'Kamera Silme İslemi', str(cameraName) +
                                                       " isimli kamerayı sistemden silmek istediğinize emin misiniz?",
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if buttonReply == QMessageBox.Yes:
                        curs.execute("DELETE FROM Cameras WHERE CameraName=?", (cameraName,))
                        conn.commit()
                        self.LoadCameraDatabase()
                    else:
                        self.LoadCameraDatabase()
                    self.show()
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def LoadCameraDatabase(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        content = """SELECT CameraName,CameraIP,CameraIPAddition,Username,Password, ProtocolType, MinPixelWidth ,
        MinPixelHeight,MinPixelArea,MinPixelRatio,MaxPixelRatio,MinDiagSize,MaxDiagSize,MaxChangeInArea,
        MaxChangeInWidth,MaxChangeInHeight,MaxAngleBetweenChar,MinNumberOfMatchCharNumber,CameraStatus,CameraLocation FROM Cameras"""
        res = conn.execute(content)
        for row_index, row_data in enumerate(res):
            self.tableWidget.insertRow(row_index)
            for colm_index, colm_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
        self.labelCameraNumber.setText("Toplam Kamera Sayısı: " + str(self.tableWidget.rowCount()))
        return

    def TableClicked(self):
        self.buttonUpdateCamera.setEnabled(True)
        self.buttonDeleteCamera.setEnabled(True)

##############################################################################################
class Fonts(QDialog,Fonts.Ui_Dialog):
    def __init__(self,parent=None):
        super(Fonts,self).__init__(parent)
        self.setupUi(self)
        self.fontName = None
        self.buttonUseFont.setToolTip("Fontu kullanmak için tıkla. Bir font seçildiği takdirde önceki iptal edilir.")
        self.buttonDeleteFont.setToolTip("""Fontu silmek için tıkla. Bir font silindiği takdirde font için "Default" değerler kullanılır""")
        try:
            self.setWindowIcon(QIcon(str(path) + "\\vagonplaka.png"))
        except Exception:
            pass
        self.setWindowTitle('Fontlar')
        self.InitUi()

    def InitUi(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.buttonDeleteFont.clicked.connect(self.DeleteFont)
        self.buttonUseFont.clicked.connect(self.UseFont)
        self.tableWidget.itemClicked.connect(self.TableClicked)
        self.buttonUseFont.setEnabled(False)
        self.buttonDeleteFont.setEnabled(False)
        self.LoadFontDatabase()

    def GetFontName(self):
        try:
            content = "SELECT * FROM Fonts"
            res = conn.execute(content)
            for row in enumerate(res):
                if row[0] == self.tableWidget.currentRow():
                    data = row[1]
                    fontName = data[1]
            return fontName
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def DeleteFont(self):
        try:
            self.buttonUseFont.setEnabled(False)
            self.buttonDeleteFont.setEnabled(False)
            fontName = self.GetFontName()
            buttonReply = QMessageBox.question(self, 'Font Silme İşlemi', str(fontName) +
                                               " isimli fontu sistemden silmek istediğinize emin misiniz?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                curs.execute("DELETE FROM Fonts WHERE FontName=?", (fontName,))
                conn.commit()
                try:
                    fontStatus = open("FontStatus.txt", "r")
                    direc = path + "Fonts\\" + str(fontName)
                    if (str(fontStatus.readline()) == direc):
                        txtfile = open("FontStatus.txt", "w")
                        txtfile.write(path + "Fonts")
                        txtfile.close()
                    shutil.rmtree(direc, ignore_errors=True)
                    self.LoadFontDatabase()
                except:
                    self.LoadFontDatabase()
            else:
                self.LoadFontDatabase()
            self.show()
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def UseFont(self):
        try:
            self.buttonUseFont.setEnabled(False)
            self.buttonDeleteFont.setEnabled(False)
            fontName = self.GetFontName()
            buttonReply = QMessageBox.question(self, 'Font Değiştirme', str(fontName) +
                                               " isimli fontu kullanmak istediğinize emin misiniz?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                txtfile = open("FontStatus.txt", "w")
                txtfile.write(path + "Fonts\\" + str(fontName))
                txtfile.close()
                self.LoadFontDatabase()
            else:
                self.LoadFontDatabase()
            self.show()
        except Exception as error:
            date = GetDate()
            filename = path + "Log\\" + date
            logToday = open(filename, "a+")
            logToday.write(str(error) + "\n")
            logToday.close()

    def TableClicked(self):
        self.buttonUseFont.setEnabled(True)
        self.buttonDeleteFont.setEnabled(True)

    def LoadFontDatabase(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        content = 'SELECT FontName,FontDate,CharCountInFont FROM Fonts'
        res = conn.execute(content)
        for row_index, row_data in enumerate(res):
            self.tableWidget.insertRow(row_index)
            for colm_index, colm_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
        return

##############################################################################################
class AddFont(QDialog,AddFont.Ui_Dialog):
    def __init__(self,parent=None):
        super(AddFont,self).__init__(parent)
        self.setupUi(self)
        self.editFontName.setToolTip("Font ismini giriniz. Boş bırakılamaz.")
        self.buttonStartRecording.setToolTip("Font fotoğrafı ve adı belirlendiyse sistem için font oluşturma işlemine başla.")
        try:
            self.setWindowIcon(QIcon(str(path) + "\\vagonplaka.png"))
        except Exception:
            pass
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Font Ekle')

##############################################################################################
class AddCamera(QDialog,AddCamera.Ui_Dialog):
    def __init__(self,parent=None):
        super(AddCamera,self).__init__(parent)
        self.setupUi(self)
        self.editCameraName.setToolTip("Kameranın sistemde görüneceği isim. Boş bırakılamaz.")
        self.editCameraIP.setToolTip("Kameraya ulaşılması için IP giriniz. (Örn. 192.168.1.1)")
        self.editCameraIPAddition.setToolTip("Kamera IP'sinin uzantısını giriniz. (Örn. axis-media/media.amp)")
        self.editUsername.setToolTip("Ulaşılacak kameranın kullanıcı adını giriniz.")
        self.editPassword.setToolTip("Ulaşılacak kameranın şifresini giriniz.")
        self.labelProtocolType.setToolTip("""Kameranın sahip olduğu protokol tipi. "Rtsp" tavsiye edilir.""")
        try:
            self.setWindowIcon(QIcon(str(path) + "vagonplaka.png"))
        except Exception:
            pass
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Kamera Ekle')

##############################################################################################
class UpdateCamera(QDialog,UpdateCamera.Ui_Dialog):
    def __init__(self,parent=None):
        super(UpdateCamera,self).__init__(parent)
        self.setupUi(self)
        self.editCameraName.setToolTip("Kameranın sistemde görüneceği isim. Boş bırakılamaz.")
        self.editCameraIP.setToolTip("Kameraya ulaşılması için IP giriniz. (Örn. 192.168.1.1)")
        self.editCameraIPAddition.setToolTip("Kamera IP'sinin uzantısını giriniz. (Örn. axis-media/media.amp)")
        self.editUsername.setToolTip("Ulaşılacak kameranın kullanıcı adını giriniz.")
        self.editPassword.setToolTip("Ulaşılacak kameranın şifresini giriniz.")
        self.labelProtocolType.setToolTip("""Kameranın sahip olduğu protokol tipi. "Rtsp" tavsiye edilir.""")
        self.editMinPixelWidth.setToolTip("Seçili alandaki her bir karakterin minimum piksel genişliği.")
        self.editMinPixelHeight.setToolTip("Seçili alandaki her bir karakterin minimum piksel yüksekliği.")
        self.editMinPixelArea.setToolTip("Seçili alandaki her bir karakterin kapladığı piksel alanı. (Genişlik x Yükseklik)")
        self.editMinPixelRatio.setToolTip("Seçili alandaki her bir karakterin minimum genişlik ve yükseklik oranı. (Genişlik / Yükseklik)")
        self.editMaxPixelRatio.setToolTip("Seçili alandaki her bir karakterin maksimum genişlik ve yükseklik oranı. (Genişlik / Yükseklik)")
        self.editMinDiagSize.setToolTip("Seçili alandaki farklı iki karakter arasındaki uzaklığın minimum çarpanı. (√a2+b2 * Çarpan)")
        self.editMaxDiagSize.setToolTip("Seçili alandaki farklı iki karakter arasındaki uzaklığın maksimum çarpanı. (√a2+b2 * Çarpan)")
        self.editMaxChangeInArea.setToolTip("Seçili alandaki her bir karakterin kapladığı piksel alanındaki kabul edilebilir maksimum tolerans değeri. (%100 = 1.0)")
        self.editMaxChangeInWidth.setToolTip("Seçili alandaki her bir karakterin tanınırken genişliğindeki kabul edilebilir maksimum tolerans değeri. (%100 = 1.0)")
        self.editMaxChangeInHeight.setToolTip("Seçili alandaki her bir karakterin tanınırken yüksekliğindeki kabul edilebilir maksimum tolerans değeri. (%100 = 1.0)")
        self.editMaxAngleBetweenChar.setToolTip("Seçili alandaki farklı iki karakter arasındaki kabul edilebilir maksimum açı. (X1-X2 / Y1-Y2)")
        self.editMinNumberOfMatchCharNumber.setToolTip("Seçili alanlardaki okunması istenen minimum karakter sayısı.")
        self.labelCameraStatus.setToolTip("Kameranın çalışma durumu. Çalışmıyor olarak belirtilen kamera sisteme dahil edilmez.")
        self.editTopY1.setToolTip("Siyah arkaplanda yyazılmış karakterlerin okunacağı alanın üst kordinatı.")
        self.editTopY2.setToolTip("Siyah arkaplanda yazılmış karakterlerin okunacağı alanın alt kordinatı.")
        self.editBottomY1.setToolTip("Beyaz arkaplanda yazılmış karakterlerin okunacağı alanın üst kordinatı.")
        self.editBottomY2.setToolTip("Beyaz arkaplanda yazılmış karakterlerin okunacağı alanın alt kordinatı.")
        try:
            self.setWindowIcon(QIcon(str(path) + "vagonplaka.png"))
        except Exception:
            pass
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Kamera Konfigürasyonu')

##############################################################################################
class Char(QDialog,Char.Ui_Dialog):
    def __init__(self,parent=None):
        super(Char,self).__init__(parent)
        self.setupUi(self)
        self.editChar.setToolTip("Seçilen karakteri girin.")
        try:
            self.setWindowIcon(QIcon(str(path) + "vagonplaka.png"))
        except Exception:
            pass
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Harf Girişi')

##############################################################################################
class AddPlateInfo(QDialog,AddPlateInfo.Ui_Dialog):
    def __init__(self,parent=None):
        super(AddPlateInfo,self).__init__(parent)
        self.setupUi(self)
        self.editTopCharCount.setToolTip("Kameranın üst kısmında görülecek plakanın karakter uzunluğu?")
        self.editTopMinCharCount.setToolTip("Kameranın üst kısmında görünen plakalardan, kaç karakterden uzun olanlar Log olarak görünsün?")
        self.editBottomCharCount.setToolTip("Kameranın alt kısmında görülecek plakanın karakter uzunluğu?")
        self.editBottomMinCharCount.setToolTip("Kameranın alt kısmında görünen plakalardan, kaç karakterden uzun olanlar Log olarak görünsün?")
        self.editControlCount.setToolTip("Kamerada görünen plaka veritabanına kaydedilmeden önce kaç kez kontrol edilsin?")
        try:
            self.setWindowIcon(QIcon(str(path) + "vagonplaka.png"))
        except Exception:
            pass
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Plaka Karakter Bilgisi')

def main():
    app = QApplication([])
    win = WagonTracking()
    try:
        win.setWindowIcon(QIcon(str(path) + "vagonplaka.png"))
    except Exception:
        pass
    app.exec_()
main()
