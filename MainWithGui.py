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
import urllib
from Interfaces.Cameras import Ui_Dialog
import Interfaces.Fonts as Fonts
import Interfaces.AddCamera as AddCamera
import Interfaces.AddFont as AddFont
import Interfaces.UpdateCamera as UpdateCamera
import Interfaces.Char as Char
from Interfaces.GUI import Ui_MainWindow
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt, QRegExp
from PyQt5.QtGui import QImage, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem,QTableWidgetItem, QFileDialog, QWidget
import sqlite3
import DetectPlateThread
import threading
import time

locale.setlocale(locale.LC_ALL, '')
conn = sqlite3.connect('PlateDetectionDB.db', check_same_thread=False)
curs = conn.cursor()
path = os.getcwd() + "/"
path = str(path)

image = None
def Screenshot(ip):
    global ret, image
    frameSize = (640, 480)
    capture = VideoStream(src=str(ip), resolution=frameSize).start()
    image = capture.read()
    capture.stream.stream.release()


##############################################################################################
class MainWithGui(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWithGui,self).__init__(parent)
        self.setupUi(self)
        self.capture = None
        self.image = None
        self.char = None
        self.fontPhoto = None
        self.checkPlateTop = None
        self.fname = None
        self.checkTop = 0
        self.txtClass = None
        self.checkPlateBottom = None
        self.listCamera = []
        self.checkBottom = 0
        self.backimage = cv2.imread(path + '/Fonts/background.png')
        self.InitUi()
        self.UpdateStatusBar()

    def InitUi(self):
        self.show()
        Database.setDatabase()

        comboboxThread = threading.Thread(target=self.FillComboBox)
        comboboxThread.daemon = True
        comboboxThread.start()

        self.LoadDatabase()
        self.startButton.clicked.connect(self.StartWebcam)
        self.startButton.setEnabled(True)
        self.stopButton.clicked.connect(self.StopWebcam)
        self.stopButton.setEnabled(False)
        self.cameraStatus = False
        self.detectButton.toggled.connect(self.DetectWebcam)
        self.detectButton.setCheckable(True)
        self.plateEnabled = False
        self.trainButton.clicked.connect(self.TrainPlates)
        self.plateTrain =False
        self.actionCameras.triggered.connect(self.ShowCamerasPage)
        self.actionAddCamera.triggered.connect(self.ShowAddCameraPage)
        self.actionFonts.triggered.connect(self.ShowFontsPage)
        self.actionAddFont.triggered.connect(self.ShowAddFont)
        self.ComboBoxCameras.setEnabled(True)
        self.detectButton.setEnabled(False)

    def UpdateStatusBar(self):
        self.statusbar.show()
        self.statusbar.showMessage("Program kullanılmaya hazır.")
        self.startButton.setStatusTip("Kameraları başlatmak için tıkla.")
        self.stopButton.setStatusTip("Kamerayı durdurmak için tıkla.")
        self.trainButton.setStatusTip("Plaka tanıma için gerekli algoritmayı sisteme yükler.")
        self.detectButton.setStatusTip("Plaka tanımayı başlatmak için tıkla. Aktif hale gelmesi için KNN taraması yapılmalı.")
        self.tableWidget.setStatusTip("Kameralarda görünen ve veritabanına kaydedilen plakalar yer alır.")
        self.tableWidget_2.setStatusTip("Listeden seçilen kamerada okunan tüm veriler yer alır.")
        self.ComboBoxCameras.setStatusTip("Sistemde var olan ve çalışır durumdaki kameralar yer alır.")

    def FillComboBox(self):
        cameraStatus = "Çalışıyor"
        while True:
            listofCameras= []
            searchall = curs.execute('SELECT CameraName FROM Cameras WHERE CameraStatus = ? ', (cameraStatus,))
            rows = searchall.fetchall()
            if(len(rows)!=0):
                for row in rows:
                    listofCameras.append(row[0])
                if(self.listCamera!=listofCameras):
                    del self.listCamera
                    self.listCamera = listofCameras.copy()
                    self.ComboBoxCameras.clear()
                    self.ComboBoxCameras.addItems(self.listCamera)
            time.sleep(5)
        
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

    def DisableButtonFontPage(self):
        if (len(self.addFontPage.editFontName.text()) > 0):
            self.addFontPage.buttonStartRecording.setEnabled(True)

    def DisableButton(self):
        if(len(self.charPage.editChar.text())>0):
            self.charPage.buttonAccept.setEnabled(True)

    def AddFontPhoto(self):
        try:
            self.fname, filter = QFileDialog().getOpenFileName(self, 'Font Fotoğrafını Seç', '', ("Image Files (*.jpg)"))
            if self.fname:
                self.LoadPhoto(self.fname)
        except Exception as error:
            self.fontPhoto = None
            QMessageBox.warning(self, 'Fotograf Uzanti Hatasi',
                                "Fotoğraf uzantısını değistirerek tekrar deneyiniz!",
                                QMessageBox.Ok, QMessageBox.Ok)

    def DetectWebcam(self, status):
        txtfile = open("ThreadStatus.txt", "w")
        if status:
            txtfile.write("True")
            txtfile.close()
            cameraStatus = "Çalışmıyor"
            self.detectButton.setText('Plaka Tanımayı Durdur')
            self.plateEnabled = True
            if(len(self.listCamera)!=0):
                for cameraName in self.listCamera:
                    print("deneme")
                    t = DetectPlateThread.camThread(cameraName)
                    t.daemon = True
                    t.start()
        else:
            txtfile.write("False")
            self.detectButton.setText('Plaka Tanimayi Baslat')
            self.plateEnabled = False

    def getIP(self):
        ip = ""
        cameraName = self.ComboBoxCameras.currentText()
        searchall = curs.execute(
            """SELECT CameraIP, CameraIPAddition, Username, Password, ProtocolType FROM Cameras WHERE CameraName = ? """,
            (cameraName,))
        rows = searchall.fetchall()
        if(rows!=None):
            for row in rows:
                cameraIP = str(row[0])
                cameraIPAddition = str(row[1])
                username = str(row[2])
                password = str(row[3])
                protocolType = str(row[4])
            if (username != "" and password != ""):
                ip = protocolType + "://" + username + ":" + password + "@" + cameraIP + "/" + cameraIPAddition
            else:
                ip = protocolType + "://" + cameraIP + "/" + cameraIPAddition
            return ip

    def StartWebcam(self):
        # self.capture = cv2.VideoCapture('rtsp://root:root@192.168.10.34/axis-media/media.amp')
        # self.capture2 = VideoStream(src='rtsp://root:root@192.168.10.49/axis-media/media.amp')
        self.ComboBoxCameras.setEnabled(False)
        self.cameraStatus = True
        ip = self.getIP()
        camera = threading.Thread(target=self.StartIPCamera, args=(ip,))
        camera.daemon = True
        camera.start()

    def StartIPCamera(self, ip):
        frameSize = (640, 480)
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.capture = VideoStream(src=ip, resolution=frameSize)
        self.capture.start()
        while self.cameraStatus == True:
            self.image = self.capture.read()
            if (len(self.image) != 0):
                self.DisplayImage(self.image)
            else:
                self.DisplayImage(self.backimage)
            if (self.plateEnabled):
                self.LoadDatabase()
        self.capture.stream.stream.release()
        self.DisplayImage(self.backimage)
        self.startButton.setEnabled(True)

    def StopWebcam(self):
        self.cameraStatus=False
        self.DisplayImage(self.backimage)
        self.ComboBoxCameras.setEnabled(True)
        if(self.plateEnabled != False):
            self.plateEnabled= False
            self.detectButton.toggle()
            self.detectButton.setText('Plaka Tanimayi Baslat')

        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)

    def TrainPlates(self):
        blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # KNN eğitimi
        if blnKNNTrainingSuccessful == False:  # Eğer KNN eğitimi başarılı değilse
            QMessageBox.warning(self, 'KNN Taramasi',
                                    "KNN taraması yapılamadı!\n",
                                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.plateTrain = True
            QMessageBox.information(self, 'KNN Taramasi',
                                    "KNN başarıyla tarandı!\n",
                                    QMessageBox.Ok, QMessageBox.Ok)

            self.detectButton.setEnabled(True)

    def StartRecording(self):
        MIN_CONTOUR_AREA = 100
        RESIZED_IMAGE_WIDTH = 20
        RESIZED_IMAGE_HEIGHT = 30
        Check = True
        if (len(str(self.addFontPage.editFontName.text())) != 0):
            fontName = str(self.addFontPage.editFontName.text())
            stream = open(self.fname, "rb")
            bytes = bytearray(stream.read())
            numpyarray = np.asarray(bytes, dtype=np.uint8)
            imgTrainingNumbers = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
            imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)
            imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)
            imgThresh = cv2.adaptiveThreshold(imgBlurred,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            imgThreshCopy = imgThresh.copy()
            npaContours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            npaFlattenedImages = np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
            charCount = 0
            intClassifications = []
            intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'),
                             ord('9'), ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'), ord('H'),
                             ord('I'), ord('J'), ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'), ord('Q'),
                             ord('R'), ord('S'), ord('T'), ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z'),
                             ord('/'), ord('-'), ord('@')]
            for npaContour in npaContours:  # for each contour
                if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:
                    [intX, intY, intW, intH] = cv2.boundingRect(npaContour)
                    cv2.rectangle(imgTrainingNumbers, (intX, intY), (intX + intW, intY + intH), (0, 0, 255), 3)
                    imgROI = imgThresh[intY:intY + intH, intX:intX + intW]
                    imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
                    self.DisplayPhoto(imgROIResized, "Char")
                    self.DisplayPhoto(imgThresh, "Thresh")
                    self.DisplayPhoto(imgTrainingNumbers, "Font")
                    self.ShowCharPage()
                    intChar = self.char
                    if intChar == None:  #ESC
                        Check = False
                        QMessageBox.warning(self, 'Çıkış',
                                            "İşlem iptal edildi!",
                                            QMessageBox.Ok, QMessageBox.Ok)
                        self.addFontPage.close()
                    if intChar in intValidChars:
                        intClassifications.append(intChar)
                        npaFlattenedImage = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
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
                        newpath = path + "Fonts" + "/" + str(fontName) + "/"
                        an = datetime.datetime.now()
                        fontDate = str(an.day) + "/" + str(an.month) + "/" + str(an.year)
                        curs.execute("""INSERT INTO Fonts(FontName, FontDate, FontFileDir, CharCountInFont) 
                                VALUES(?,?,?,?)""", (fontName, str(fontDate), newpath, str(charCount)))
                        conn.commit()
                        charCount = 0
                        os.makedirs(newpath)
                        np.savetxt(newpath + "classifications.txt",
                                   npaClassifications)  # write flattened images to file
                        np.savetxt(newpath + "flattened_images.txt", npaFlattenedImages)  #
                        self.char == None
                        self.addFontPage.close()
                        QMessageBox.information(self, 'Kayıt Başarılı',
                                                "Font için sınıflandırma ve fotoğraf dizeleri başarıyla oluşturuldu.",
                                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, 'Font İsim Hatası',
                                "Lütfen font için isim giriniz!",
                                QMessageBox.Ok, QMessageBox.Ok)

    def GetCharInfo(self):
        char = self.charPage.editChar.text()
        if (char != ""):
            self.char = ord(char)
            self.char = int(self.char)
            self.charPage.close()
        else:
            self.charPage.close()
            self.addFontPage.close()
            QMessageBox.warning(self, 'Harf Hatasi',
                                "Lütfen tekrar deneyiniz!",
                                QMessageBox.Ok, QMessageBox.Ok)

    def LoadPhoto(self, fname):
        stream = open(fname, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        self.fontPhoto = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        self.DisplayPhoto(self.fontPhoto, "Font")

    def AddCamera(self):
        cameraName = self.addCameraPage.editCameraName.text()
        cameraIP = self.addCameraPage.editCameraIP.text()
        cameraIPAddition = self.addCameraPage.editCameraIPAddition.text()
        username = self.addCameraPage.editUsername.text()
        password = self.addCameraPage.editPassword.text()
        protocolType = "rtsp"
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
        search = curs.execute('SELECT CameraName FROM Cameras WHERE CameraName = ? ', (cameraName,))
        results = search.fetchone()
        if (len(cameraIP) < 16 and len(cameraIP) > 0 and cameraName != ""):
            if (results == None):
                if (self.addCameraPage.radioButtonRtsp.isChecked() == True):
                    protocolType = "rtsp"
                if (self.addCameraPage.radioButtonHttp.isChecked() == True):
                    protocolType = "http"
                curs.execute("""INSERT INTO Cameras(CameraName,CameraIP,CameraIPAddition,Username,Password, 
                ProtocolType, MinPixelWidth ,MinPixelHeight,MinPixelArea,MinPixelRatio,MaxPixelRatio,MinDiagSize,
                MaxDiagSize,MaxChangeInArea,MaxChangeInWidth,MaxChangeInHeight,MaxAngleBetweenChar,MinNumberOfMatchCharNumber,
                TopYOne,TopYTwo,BottomYOne,BottomYTwo,CameraStatus) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                cameraName, cameraIP, cameraIPAddition, username, password, protocolType, minPixelWidth, minPixelHeight,
                minPixelArea, minPixelRatio, maxPixelRatio, minDiagSize, maxDiagSize, maxChangeInArea, maxChangeInWidth,
                maxChangeInHeight, maxAngleBetweenChar, minNumberOfMatchCharNumber, topYOne, topYTwo, bottomYOne,
                bottomYTwo, cameraStatus))
                conn.commit()
                protocolType = "rtsp"
                self.addCameraPage.close()
                QMessageBox.information(self, 'Kayit Basarili!',
                                        "Kamera sisteme eklendi!\n",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self, 'Gecersiz Kamera İsmi!',
                                    "Eklenmek istenen kamera adı sistemde mevcut!\n",
                                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, 'Gecersiz Bilgi!',
                                "Eklenmek istenen bilgileri kontrol ediniz!\n",
                                QMessageBox.Ok, QMessageBox.Ok)

    def LoadDatabase(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        content = 'SELECT Plate,Date,Time FROM Plates'
        res = conn.execute(content)
        for row_index, row_data in enumerate(res):
            self.tableWidget.insertRow(row_index)
            for colm_index, colm_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
        return

    def DisplayImage(self, img):
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

    def DisplayPhoto(self, img,type):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:  # [0]=satırlar, [1]=sütunlar, [2]=kanallar
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
            self.setWindowIcon(QIcon(str(path) + "/vagonplaka.png"))
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
            self.backimage= cv2.imread(path + 'Fonts/background.png')
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
        self.updateCameraPage.buttonShowCounters.clicked.connect(self.Counters)
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

    def AddCamera(self):
        cameraName = self.addCameraPage.editCameraName.text()
        cameraIP = self.addCameraPage.editCameraIP.text()
        cameraIPAddition = self.addCameraPage.editCameraIPAddition.text()
        username = self.addCameraPage.editUsername.text()
        password = self.addCameraPage.editPassword.text()
        protocolType = "rtsp"
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
        search = curs.execute('SELECT CameraName FROM Cameras WHERE CameraName = ? ', (cameraName,))
        results = search.fetchone()
        if (len(cameraIP) < 16 and len(cameraIP) > 0 and cameraName != ""):
            if (results == None):
                if (self.addCameraPage.radioButtonRtsp.isChecked() == True):
                    protocolType = "rtsp"
                if (self.addCameraPage.radioButtonHttp.isChecked() == True):
                    protocolType = "http"
                curs.execute("""INSERT INTO Cameras(CameraName,CameraIP,CameraIPAddition,Username,Password, 
                                ProtocolType, MinPixelWidth ,MinPixelHeight,MinPixelArea,MinPixelRatio,MaxPixelRatio,MinDiagSize,
                                MaxDiagSize,MaxChangeInArea,MaxChangeInWidth,MaxChangeInHeight,MaxAngleBetweenChar,MinNumberOfMatchCharNumber,
                                TopYOne,TopYTwo,BottomYOne,BottomYTwo,CameraStatus) 
                                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                    cameraName, cameraIP, cameraIPAddition, username, password, protocolType, minPixelWidth,
                    minPixelHeight,
                    minPixelArea, minPixelRatio, maxPixelRatio, minDiagSize, maxDiagSize, maxChangeInArea,
                    maxChangeInWidth,
                    maxChangeInHeight, maxAngleBetweenChar, minNumberOfMatchCharNumber, topYOne, topYTwo, bottomYOne,
                    bottomYTwo, cameraStatus))
                conn.commit()
                self.LoadCameraDatabase()
                protocolType = "rtsp"
                self.addCameraPage.close()
                QMessageBox.information(self, 'Kayit Basarili!',
                                        "Kamera sisteme eklendi!\n",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self, 'Gecersiz Kamera İsmi!',
                                    "Eklenmek istenen kamera adı sistemde mevcut!\n",
                                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, 'Gecersiz Bilgi!',
                                "Eklenmek istenen bilgileri kontrol ediniz!\n",
                                QMessageBox.Ok, QMessageBox.Ok)

    def CounterSize(self,topYOne,topYTwo,bottomYOne,bottomYTwo):
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

    def Counters(self):
        cameraIP = self.updateCameraPage.editCameraIP.text()
        cameraIPAddition = self.updateCameraPage.editCameraIPAddition.text()
        username = self.updateCameraPage.editUsername.text()
        password = self.updateCameraPage.editPassword.text()
        topYOne = self.updateCameraPage.editTopY1.text()
        topYTwo = self.updateCameraPage.editTopY2.text()
        bottomYOne = self.updateCameraPage.editBottomY1.text()
        bottomYTwo = self.updateCameraPage.editBottomY2.text()
        topYOne, topYTwo, bottomYOne, bottomYTwo =self.CounterSize(topYOne, topYTwo, bottomYOne, bottomYTwo)
        protocolType = "rtsp"
        if (self.updateCameraPage.radioButtonRtsp.isChecked() == True):
            protocolType = "rtsp"
        if (self.updateCameraPage.radioButtonHttp.isChecked() == True):
            protocolType = "http"
        if (username != "" and password != ""):
            ip = str(protocolType) + "://" + str(username) + ":" + str(password) + "@" + str(cameraIP) + "/" + cameraIPAddition
        else:
            ip = str(protocolType) + "://" + str(cameraIP) + "/" + cameraIPAddition
        self.GetFrameFromCamera(ip, topYOne, topYTwo, bottomYOne, bottomYTwo)

    def GetFrameFromCamera(self, ip, topYOne, topYTwo, bottomYOne, bottomYTwo):
        global image
        deneme = threading.Thread(target=Screenshot, args=(ip,))
        deneme.daemon = True
        deneme.start()
        if (image != None):
            img = self.ShowCounters(image, topYOne, topYTwo, bottomYOne, bottomYTwo)
            self.DisplayPhoto(img)
        else:
            self.DisplayPhoto(self.backimage)
            self.updateCameraPage.buttonShowCounters.setEnabled(False)
            QMessageBox.warning(self, 'Kamera Hatası!',
                                "Ulaşılmak istenen kameraya erişim sağlanamadı. Lütfen bilgileri kontrol ediniz!\n" + "IP: " + ip + "\n",
                                QMessageBox.Ok, QMessageBox.Ok)


    def ShowCounters(self,img,topyone,topytwo,bottomyone,bottomytwo):
        cv2.rectangle(img, (0, int(topyone)), (640, int(topytwo)), (255, 0, 0), 2)
        cv2.rectangle(img, (0, int(bottomyone)), (640, int(bottomytwo)), (0, 0, 255), 2)
        return img

    def ShowCameraData(self):
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
                self.updateCameraPage.editCameraName.setText(str(cameraName))
                self.updateCameraPage.editCameraIP.setText(str(cameraIP))
                self.updateCameraPage.editCameraIPAddition.setText(str(cameraIPAddition))
                self.updateCameraPage.editUsername.setText(str(username))
                self.updateCameraPage.editPassword.setText(str(password))
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
                if(protocolType=="rtsp"):
                    self.updateCameraPage.radioButtonRtsp.setChecked(True)
                if(protocolType=="http"):
                    self.updateCameraPage.radioButtonHttp.setChecked(True)
                if(cameraStatus=="Çalışıyor"):
                    self.updateCameraPage.radioButtonWorking.setChecked(True)
                    self.GetFrameFromCamera(ip, topYOne, topYTwo, bottomYOne, bottomYTwo)
                if(cameraStatus=="Çalışmıyor"):
                    self.updateCameraPage.radioButtonNotWorking.setChecked(True)
                    self.updateCameraPage.buttonShowCounters.setEnabled(False)



    def UpdateCamera(self):
        global image
        cameraName = self.updateCameraPage.editCameraName.text()
        cameraIP = self.updateCameraPage.editCameraIP.text()
        cameraIPAddition = self.updateCameraPage.editCameraIPAddition.text()
        username = self.updateCameraPage.editUsername.text()
        password = self.updateCameraPage.editPassword.text()
        minPixelWidth = self.updateCameraPage.editMinPixelWidth.text()
        minPixelHeight = self.updateCameraPage.editMinPixelHeight.text()
        minPixelArea = self.updateCameraPage.editMinPixelArea.text()
        minPixelRatio =  str(float(self.updateCameraPage.editMinPixelRatio.text()))
        maxPixelRatio = str(float(self.updateCameraPage.editMaxPixelRatio.text()))
        minDiagSize = str(float(self.updateCameraPage.editMinDiagSize.text()))
        maxDiagSize = str(float(self.updateCameraPage.editMaxDiagSize.text()))
        maxChangeInArea = str(float(self.updateCameraPage.editMaxChangeInArea.text()))
        maxChangeInWidth = str(float(self.updateCameraPage.editMaxChangeInWidth.text()))
        maxChangeInHeight = str(float(self.updateCameraPage.editMaxChangeInHeight.text()))
        maxAngleBetweenChar = str(float(self.updateCameraPage.editMaxAngleBetweenChar.text()))
        minNumberOfMatchCharNumber = self.updateCameraPage.editMinNumberOfMatchCharNumber.text()
        topYOne = self.updateCameraPage.editTopY1.text()
        topYTwo = self.updateCameraPage.editTopY2.text()
        bottomYOne = self.updateCameraPage.editBottomY1.text()
        bottomYTwo = self.updateCameraPage.editBottomY2.text()
        topYOne, topYTwo, bottomYOne, bottomYTwo = self.CounterSize(topYOne, topYTwo, bottomYOne, bottomYTwo)
        protocolType = "rtsp"
        cameraStatus = "Çalışmıyor"
        if(self.updateCameraPage.radioButtonRtsp.isChecked()==True):
            protocolType = "rtsp"
        if(self.updateCameraPage.radioButtonHttp.isChecked()==True):
            protocolType = "http"
        if(self.updateCameraPage.radioButtonWorking.isChecked()==True):
            cameraStatus = "Çalışıyor"
        if(self.updateCameraPage.radioButtonNotWorking.isChecked()==True):
            cameraStatus = "Çalışmıyor"
        search = curs.execute('SELECT CameraName FROM Cameras WHERE CameraName = ? ', (cameraName,))
        searchTwo = curs.execute('SELECT CameraName FROM Cameras WHERE CameraName = ? ', (cameraName.lower(),))
        results = search.fetchone()
        resultsTwo = search.fetchone()
        if(str(self.oldCameraName).lower() == cameraName.lower()):
            curs.execute("""UPDATE Cameras SET CameraName = ? , CameraIP = ? , CameraIPAddition = ? , Username = ? , Password = ? , 
                ProtocolType = ? , MinPixelWidth = ? , MinPixelHeight = ? , MinPixelArea = ? , MinPixelRatio = ? , 
                MaxPixelRatio = ? , MinDiagSize = ? , MaxDiagSize = ? , MaxChangeInArea = ? , MaxChangeInWidth = ? , 
                MaxChangeInHeight = ? , MaxAngleBetweenChar = ? , MinNumberOfMatchCharNumber = ? , TopYOne = ? , 
                TopYTwo = ? , BottomYOne = ? , BottomYTwo = ? , CameraStatus = ? WHERE CameraName = ?""",
                (cameraName, cameraIP, cameraIPAddition, username, password, protocolType, minPixelWidth, minPixelHeight, minPixelArea, minPixelRatio, maxPixelRatio, minDiagSize, maxDiagSize, maxChangeInArea, maxChangeInWidth, maxChangeInHeight, maxAngleBetweenChar, minNumberOfMatchCharNumber, topYOne, topYTwo, bottomYOne, bottomYTwo, cameraStatus, self.oldCameraName))
            conn.commit()
            image = None
            self.LoadCameraDatabase()
            self.updateCameraPage.close()
            QMessageBox.information(self, 'Guncelleme Basarili!',
                                    "Kamera konfigürasyon güncellemesi başarı ile yapıldı!",
                                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            if (results == None and resultsTwo == None):
                curs.execute("""UPDATE Cameras SET CameraName = ? , CameraIP = ? , CameraIPAddition = ? , Username = ? , Password = ? , 
                                ProtocolType = ? , MinPixelWidth = ? , MinPixelHeight = ? , MinPixelArea = ? , MinPixelRatio = ? , 
                                MaxPixelRatio = ? , MinDiagSize = ? , MaxDiagSize = ? , MaxChangeInArea = ? , MaxChangeInWidth = ? , 
                                MaxChangeInHeight = ? , MaxAngleBetweenChar = ? , MinNumberOfMatchCharNumber = ? , TopYOne = ? , 
                                TopYTwo = ? , BottomYOne = ? , BottomYTwo = ?, CameraStatus = ? WHERE CameraName = ?""",
                             (cameraName, cameraIP, cameraIPAddition, username, password, protocolType, minPixelWidth,
                              minPixelHeight, minPixelArea, minPixelRatio, maxPixelRatio, minDiagSize, maxDiagSize,
                              maxChangeInArea, maxChangeInWidth, maxChangeInHeight, maxAngleBetweenChar,
                              minNumberOfMatchCharNumber, topYOne, topYTwo, bottomYOne, bottomYTwo, cameraStatus, self.oldCameraName))
                conn.commit()
                self.LoadCameraDatabase()
                self.updateCameraPage.close()
                QMessageBox.information(self, 'Güncelleme Başarılı!',
                                        "Kamera konfigürasyon güncellemesi başarı ile yapıldı!\n",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self, 'Güncelleme Hatası!',
                                    "Girilen kamera ismi sistemde mevcut!\n",
                                    QMessageBox.Ok, QMessageBox.Ok)

    def DisplayPhoto(self, img):
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

    def DeleteCamera(self):
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

    def LoadCameraDatabase(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        content = """SELECT CameraName,CameraIP,CameraIPAddition,Username,Password, ProtocolType, MinPixelWidth ,
        MinPixelHeight,MinPixelArea,MinPixelRatio,MaxPixelRatio,MinDiagSize,MaxDiagSize,MaxChangeInArea,
        MaxChangeInWidth,MaxChangeInHeight,MaxAngleBetweenChar,MinNumberOfMatchCharNumber,CameraStatus FROM Cameras"""
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
        try:
            self.setWindowIcon(QIcon(str(path) + "/vagonplaka.png"))
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
        content = "SELECT * FROM Fonts"
        res = conn.execute(content)
        for row in enumerate(res):
            if row[0] == self.tableWidget.currentRow():
                data = row[1]
                fontName = data[1]
        return fontName

    def DeleteFont(self):
        self.buttonUseFont.setEnabled(False)
        self.buttonDeleteFont.setEnabled(False)
        fontName = self.GetFontName()
        buttonReply = QMessageBox.question(self, 'Font Silme İşlemi', str(fontName) +
                                           " isimli fontu sistemden silmek istediğinize emin misiniz?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            curs.execute("DELETE FROM Fonts WHERE FontName=?", (fontName,))
            conn.commit()
            fontStatus = open("FontStatus.txt", "r")
            direc = path + "Fonts/" + str(fontName)
            if (str(fontStatus.readline()) == direc):
                txtfile = open("FontStatus.txt", "w")
                txtfile.write(path + "Fonts")
                txtfile.close()
            shutil.rmtree(direc, ignore_errors=True)
            self.LoadFontDatabase()
        else:
            self.LoadFontDatabase()
        self.show()

    def UseFont(self):
        self.buttonUseFont.setEnabled(False)
        self.buttonDeleteFont.setEnabled(False)
        fontName = self.GetFontName()
        buttonReply = QMessageBox.question(self, 'Font Değiştirme', str(fontName) +
                                           " isimli fontu kullanmak istediğinize emin misiniz?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            txtfile = open("FontStatus.txt", "w")
            txtfile.write(path + "Fonts/" +str(fontName))
            txtfile.close()
            self.LoadFontDatabase()
        else:
            self.LoadFontDatabase()
        self.show()

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
        try:
            self.setWindowIcon(QIcon(str(path) + "/vagonplaka.png"))
        except Exception:
            pass
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Font Ekle')

##############################################################################################
class AddCamera(QDialog,AddCamera.Ui_Dialog):
    def __init__(self,parent=None):
        super(AddCamera,self).__init__(parent)
        self.setupUi(self)
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
        try:
            self.setWindowIcon(QIcon(str(path) + "vagonplaka.png"))
        except Exception:
            pass
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Kamera Bilgilerini Güncelle')

##############################################################################################
class Char(QDialog,Char.Ui_Dialog):
    def __init__(self,parent=None):
        super(Char,self).__init__(parent)
        self.setupUi(self)
        try:
            self.setWindowIcon(QIcon(str(path) + "vagonplaka.png"))
        except Exception:
            pass
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Harf Giriş Ekranı')

def main():
    app = QApplication([])
    win = MainWithGui()
    try:
        win.setWindowIcon(QIcon(str(path) + "vagonplaka.png"))
    except Exception:
        pass
    app.exec_()

main()
