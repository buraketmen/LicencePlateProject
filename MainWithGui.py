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
import FontGenerator
import Database
import datetime
import shutil
from Cameras import Ui_Dialog
import Fonts
import AddCamera
import AddFont
import UpdateCamera
import Char
from GUI import Ui_MainWindow
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt, QRegExp
from PyQt5.QtGui import QImage, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem,QTableWidgetItem, QFileDialog, QWidget
import sqlite3

locale.setlocale(locale.LC_ALL, '')
conn = sqlite3.connect('PlateDetectionDB.db')
curs = conn.cursor()

#curs.execute("DELETE FROM Plates")
def Screenshot(ip):
    capture = VideoStream(src=str(ip))
    try:
        frame = capture.read()
        return frame
    except:
        pass

class MainWithGui(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWithGui,self).__init__(parent)
        self.setupUi(self)
        self.capture = None
        self.capture2 = None
        self.image = None
        self.char = None
        self.fontPhoto = None
        self.checkPlateTop = None
        self.fname = None
        self.checkTop = 0
        self.txtClass = None
        self.checkPlateBottom = None
        self.checkBottom = 0
        try:
            self.backimage= cv2.imread('background.jpg')
        except:
            pass
        self.InitUi()

    def InitUi(self):
        self.show()
        Database.setDatabase()
        self.startButton.clicked.connect(self.startWebcam)
        self.startButton.setEnabled(True)
        self.stopButton.clicked.connect(self.stopWebcam)
        self.stopButton.setEnabled(False)
        self.cameraStatus = False
        self.detectButton.toggled.connect(self.detectWebcam)
        self.detectButton.setCheckable(True)
        self.detectButton.setEnabled(False)
        self.plateEnabled = False
        self.trainButton.clicked.connect(self.trainPlates)
        self.plateTrain =False
        
        self.actionCameras.triggered.connect(self.ShowCamerasPage)
        self.actionAddCamera.triggered.connect(self.ShowAddCameraPage)
        self.actionFonts.triggered.connect(self.ShowFontsPage)
        self.actionAddFont.triggered.connect(self.ShowAddFont)
        
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

    def StartRecording(self):
        MIN_CONTOUR_AREA = 100
        RESIZED_IMAGE_WIDTH = 20
        RESIZED_IMAGE_HEIGHT = 30
        Check = True
        if(len(str(self.addFontPage.editFontName.text()))!=0):
            fontName = str(self.addFontPage.editFontName.text())
            stream = open(self.fname, "rb")
            bytes = bytearray(stream.read())
            numpyarray = np.asarray(bytes, dtype=np.uint8)
            imgTrainingNumbers = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
            imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)  # get grayscale image
            imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)  # blur

            # filter image from grayscale to black and white
            imgThresh = cv2.adaptiveThreshold(imgBlurred,  # input image
                                              255,  # make pixels that pass the threshold full white
                                              cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              # use gaussian rather than mean, seems to give better results
                                              cv2.THRESH_BINARY_INV, 11, 2)  # constant subtracted from the mean or weighted mean

            imgThreshCopy = imgThresh.copy()  # make a copy of the thresh image, this in necessary b/c findContours modifies the image

            npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,
                                                         # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                         cv2.RETR_EXTERNAL,  # retrieve the outermost contours only
                                                         cv2.CHAIN_APPROX_SIMPLE)  # compress horizontal, vertical, and diagonal segments and leave only their end points

            npaFlattenedImages = np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
            charCount = 0
            intClassifications = []  # declare empty classifications list, this will be our list of how we are classifying our chars from user input, we will write to file at the end

            # possible chars we are interested in are digits 0 through 9, put these in list intValidChars
            intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'),
                             ord('9'),ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'), ord('H'),
                             ord('I'), ord('J'), ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'), ord('Q'),
                             ord('R'), ord('S'), ord('T'), ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z')]
            for npaContour in npaContours:  # for each contour

                if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:  # if contour is big enough to consider
                    [intX, intY, intW, intH] = cv2.boundingRect(npaContour)  # get and break out bounding rect

                    # draw rectangle around each contour as we ask user for input
                    cv2.rectangle(imgTrainingNumbers,  (intX, intY), (intX + intW, intY + intH),  (0, 0, 255), 3)
                    imgROI = imgThresh[intY:intY + intH, intX:intX + intW]  # crop char out of threshold image
                    imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH,
                                                        RESIZED_IMAGE_HEIGHT))  # resize image, this will be more consistent for recognition and storage

                    self.displayPhoto(imgROIResized,"Char")
                    self.displayPhoto(imgThresh, "Thresh")
                    self.displayPhoto(imgTrainingNumbers,"Font")
                    self.ShowCharPage()
                    intChar = self.char
                    if intChar == None:  # if esc key was pressed
                        Check = False
                        QMessageBox.warning(self, 'Çıkış',
                                            "İşlem iptal edildi!",
                                            QMessageBox.Ok, QMessageBox.Ok)
                        self.addFontPage.close()
                    if intChar in intValidChars:  # else if the char is in the list of chars we are looking for . . .
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
                        path = "./Fonts" + "/" + str(fontName) + "/"
                        an = datetime.datetime.now()
                        fontDate = str(an.day) + "/" + str(an.month) + "/" + str(an.year)
                        curs.execute("""INSERT INTO Fonts(FontName, FontDate, FontFileDir, CharCountInFont) 
                                VALUES(?,?,?,?)""", (fontName, str(fontDate), path, str(charCount)))
                        conn.commit()
                        os.makedirs(path)
                        np.savetxt(path + "classifications.txt", npaClassifications)  # write flattened images to file
                        np.savetxt(path + "flattened_images.txt", npaFlattenedImages)  #
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
        char =self.charPage.editChar.text()
        if(char!=""):
            self.char = ord(char)
            self.char = int(self.char)
            self.charPage.close()
        else:
            self.charPage.close()
            self.addFontPage.close()
            QMessageBox.warning(self, 'Harf Hatasi',
                                "Lütfen tekrar deneyiniz!",
                                QMessageBox.Ok, QMessageBox.Ok)

    def LoadPhoto(self,fname):
        stream = open(fname, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        self.fontPhoto = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        self.displayPhoto(self.fontPhoto,"Font")

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
        topYOne = 0
        topYTwo = 240
        bottomYOne = 240
        bottomYTwo = 480
        search = curs.execute('SELECT CameraName FROM Cameras WHERE CameraName = ? ', (cameraName,))
        results = search.fetchone()
        if(len(cameraIP)<16 and len(cameraIP)>0 and cameraName!=""):
            if(results == None):
                if(self.addCameraPage.radioButtonRtsp.isChecked()==True):
                    protocolType = "rtsp"
                if(self.addCameraPage.radioButtonHttp.isChecked()==True):
                    protocolType = "http"
                    
                curs.execute("""INSERT INTO Cameras(CameraName,CameraIP,CameraIPAddition,Username,Password, ProtocolType, MinPixelWidth ,MinPixelHeight,MinPixelArea,MinPixelRatio,MaxPixelRatio,MinDiagSize,MaxDiagSize,MaxChangeInArea,MaxChangeInWidth,MaxChangeInHeight,MaxAngleBetweenChar,MinNumberOfMatchCharNumber,TopYOne,TopYTwo,BottomYOne,BottomYTwo) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(cameraName, cameraIP, cameraIPAddition, username, password, protocolType, minPixelWidth, minPixelHeight, minPixelArea,minPixelRatio, maxPixelRatio, minDiagSize, maxDiagSize, maxChangeInArea, maxChangeInWidth, maxChangeInHeight , maxAngleBetweenChar, minNumberOfMatchCharNumber,topYOne,topYTwo,bottomYOne, bottomYTwo))
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

    def detectWebcam(self, status):
        if status:
            self.detectButton.setText('Plaka Tanımayı Durdur')
            self.plateEnabled = True
        else:
            self.detectButton.setText('Plaka Tanimayi Baslat')
            self.plateEnabled = False

    def startWebcam(self):
        try:
            # self.capture = cv2.VideoCapture('rtsp://root:root@192.168.10.34/axis-media/media.amp')
            #'rtsp://root:root@192.168.10.34/axis-media/media.amp'
            #self.capture = cv2.VideoCapture(0)
            self.capture = VideoStream(src='rtsp://root:root@192.168.10.34/axis-media/media.amp') #imutils
            #self.capture2 = VideoStream(src='rtsp://root:root@192.168.10.49/axis-media/media.amp')

            self.capture.start() #imutils
            #self.capture2.start()
            frame = self.capture.read() #kontrol
        except:
            self.startButton.setEnabled(False)
            QMessageBox.warning(self, 'Kamera Hatasi!',
                                "Sistemde herhangi bir kamera bulunamadi.\n",
                                QMessageBox.Ok, QMessageBox.Ok)
        if(self.capture!=None):
            self.cameraStatus=True
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            self.trainButton.setEnabled(False)
            if(self.plateTrain==True):
                self.detectButton.setEnabled(True)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateFrame)
            self.timer.start(1)

            self.statusbar.showMessage('Kamera baslatildi.')


    def stopWebcam(self):
        self.cameraStatus=False
        if(self.plateEnabled != False):
            self.plateEnabled= False
            self.detectButton.toggle()
            self.detectButton.setText('Plaka Tanimayi Baslat')
        self.timer.stop()
        self.displayImage(self.backimage)
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.detectButton.setEnabled(False)
        self.trainButton.setEnabled(True)
            

    def trainPlates(self):
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
        if (self.cameraStatus == True):
            self.detectButton.setEnabled(True)

    def updateFrame(self):
        self.image = self.capture.read()
        if (self.plateEnabled):
            detectedImage = self.detectPlate(self.image)
            self.displayImage(detectedImage)
        else:
            self.displayImage(self.image)

    def detectPlate(self, img):
        imgtop = self.image[0:240, 0:640]
        imgbottom = self.image[240:480, 0:640]
        cv2.rectangle(img, (10, 10), (630, 240), (0, 255, 0), 1)
        cv2.rectangle(img, (10, 250), (630, 470), (0, 0, 255), 1)

        listOfPossiblePlatesTop = DetectPlates.detectPlatesInScene(imgtop,2)  # Plakaları tespit et
        listOfPossiblePlatesTop = DetectChars.detectCharsInPlates(listOfPossiblePlatesTop,2)  # Plaka içindeki karakterleri tespit et

        listOfPossiblePlatesBottom = DetectPlates.detectPlatesInScene(imgbottom, 1)  # Plakaları tespit et
        listOfPossiblePlatesBottom = DetectChars.detectCharsInPlates(listOfPossiblePlatesBottom,1)  # Plaka içindeki karakterleri tespit et
        if (len(listOfPossiblePlatesTop) != 0):
            # Eğer program buraya geldiyse en azından bir plaka okunmuştur
            # Olası plakaların listesini DESCENDING sıralamasına göre sırala (Çok karakterden az karaktere)
            listOfPossiblePlatesTop.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
            licPlateTop = listOfPossiblePlatesTop[0]
            if(len(licPlateTop.strChars)>4):
                print(licPlateTop.strChars)
            if (len(licPlateTop.strChars) == 8):
                if (self.checkPlateTop == licPlateTop.strChars):
                    self.checkTop += 1
                else:
                    self.checkTop = 0
                if (self.checkTop == 5):
                    self.Add2Database(licPlateTop.strChars, licPlateTop.imgPlate, licPlateTop.imgThresh, imgtop)
                self.checkPlateTop = licPlateTop.strChars
            if (len(listOfPossiblePlatesBottom) != 0):
                listOfPossiblePlatesBottom.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
                # Tanınmış karakterlere sahip plakanın (dize uzunluğu azalan şekilde ilk plaka) gerçek olduğunu varsay
                licPlateBottom = listOfPossiblePlatesBottom[0]
                if (len(licPlateBottom.strChars) > 10):
                    print(licPlateBottom.strChars)
                if (len(licPlateBottom.strChars) == 12):
                    if (self.checkPlateBottom == licPlateBottom.strChars):
                        self.checkBottom += 1
                    else:
                        self.checkBottom = 0
                    if (self.checkBottom == 5):
                        self.Add2Database(licPlateBottom.strChars, licPlateBottom.imgPlate,
                                          licPlateBottom.imgThresh, imgbottom)
                    self.checkPlateBottom = licPlateBottom.strChars
        return img

    def Add2Database(self,plate,imgPlate,imgThresh,img):
        an = datetime.datetime.now()
        second = int(an.second)
        hour = int(an.hour)
        date = str(an.day) + "." + str(an.month) + "." + str(an.year)
        time = str(an.hour) + "." + str(an.minute) + "." + str(an.second)
        searchall = curs.execute('SELECT Plate FROM Plates WHERE Plate = ? AND Date =?', (plate,date,))
        rows = searchall.fetchall()
        i=0
        if(rows!=None):
            for row in rows:
                i=i+1
        if(i==0):
            try:
                #cv2.imwrite("./PlatePhotos/Original_{}_{}_{}.png".format(plate,date,time),imgPlate)  # Kırpılan plakayı ve işlenmiş halini kaydet
                cv2.imwrite("./PlatePhotos/Thresh_{}_{}_{}.png".format(plate,date,time), imgThresh)
            except:
                pass
            curs.execute("INSERT INTO Plates (Plate,Date,Time) VALUES(?,?,?)",
                         (plate, date, time))
            conn.commit()
            self.Load_Database()

    def Load_Database(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        content = 'SELECT Plate,Date,Time FROM Plates'
        res = conn.execute(content)
        for row_index, row_data in enumerate(res):
            self.tableWidget.insertRow(row_index)
            for colm_index, colm_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
        return

    def displayImage(self, img):
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

    def displayPhoto(self, img,type):
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
        self.setWindowTitle('Kameralar')
        self.loadCameraDatabase()
        self.InitUi()
        self.topYone= 0
        self.topYtwo= 240
        self.bottomYone = 240
        self.bottomYtwo = 480
        try:
            self.backimage= cv2.imread('background.jpg')
        except:
            pass
        self.bottomYtwo =480
        self.oldCameraName = None

    def InitUi(self):
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

                curs.execute("""INSERT INTO Cameras(CameraName,CameraIP,CameraIPAddition,Username,Password, ProtocolType, MinPixelWidth ,MinPixelHeight,MinPixelArea,MinPixelRatio,MaxPixelRatio,MinDiagSize,MaxDiagSize,MaxChangeInArea,MaxChangeInWidth,MaxChangeInHeight,MaxAngleBetweenChar,MinNumberOfMatchCharNumber,TopYOne,TopYTwo,BottomYOne,BottomYTwo) 
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                cameraName, cameraIP, cameraIPAddition, username, password, protocolType, minPixelWidth, minPixelHeight,
                minPixelArea, minPixelRatio, maxPixelRatio, minDiagSize, maxDiagSize, maxChangeInArea, maxChangeInWidth,
                maxChangeInHeight, maxAngleBetweenChar, minNumberOfMatchCharNumber, topYOne, topYTwo, bottomYOne,
                bottomYTwo))
                conn.commit()
                self.loadCameraDatabase()
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

    def GetFrameFromCamera(self,ip, topYOne, topYTwo, bottomYOne, bottomYTwo):
        image = Screenshot(ip)
        try:
            if len(image.shape) == 3:
                if (image.shape[2]) == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888
            img = self.ShowCounters(image, topYOne, topYTwo, bottomYOne, bottomYTwo)
            self.displayPhoto(img)
        except:
            self.displayPhoto(self.backimage)
            self.updateCameraPage.buttonShowCounters.setEnabled(False)
            QMessageBox.warning(self, 'Gecersiz Kamera İşlemi!',
                                "Ulaşılmak istenen kameranın bilgileri hatalı!\n",
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
                if(protocolType=="rtsp"):
                    self.updateCameraPage.radioButtonRtsp.setChecked(True)
                if(protocolType=="http"):
                    self.updateCameraPage.radioButtonHttp.setChecked(True)
                if(username!="" and password!=""):
                    ip = str(protocolType)+"://"+str(username)+":"+str(password)+"@"+ str(cameraIP)+"/"+cameraIPAddition
                else:
                    ip = str(protocolType) + "://" + str(cameraIP) + "/" + cameraIPAddition
                self.GetFrameFromCamera(ip, topYOne, topYTwo, bottomYOne, bottomYTwo)

    def UpdateCamera(self):
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
        if(self.updateCameraPage.radioButtonRtsp.isChecked()==True):
            protocolType = "rtsp"
        if(self.updateCameraPage.radioButtonHttp.isChecked()==True):
            protocolType = "http"
        search = curs.execute('SELECT CameraName FROM Cameras WHERE CameraName = ? ', (cameraName,))
        searchTwo = curs.execute('SELECT CameraName FROM Cameras WHERE CameraName = ? ', (cameraName.lower(),))
        results = search.fetchone()
        resultsTwo = search.fetchone()
        if(str(self.oldCameraName).lower() == cameraName.lower()):
            curs.execute("""UPDATE Cameras SET CameraName = ? , CameraIP = ? , CameraIPAddition = ? , Username = ? , Password = ? , 
                ProtocolType = ? , MinPixelWidth = ? , MinPixelHeight = ? , MinPixelArea = ? , MinPixelRatio = ? , 
                MaxPixelRatio = ? , MinDiagSize = ? , MaxDiagSize = ? , MaxChangeInArea = ? , MaxChangeInWidth = ? , 
                MaxChangeInHeight = ? , MaxAngleBetweenChar = ? , MinNumberOfMatchCharNumber = ? , TopYOne = ? , 
                TopYTwo = ? , BottomYOne = ? , BottomYTwo = ? WHERE CameraName = ?""",
                (cameraName, cameraIP, cameraIPAddition, username, password, protocolType, minPixelWidth, minPixelHeight, minPixelArea, minPixelRatio, maxPixelRatio, minDiagSize, maxDiagSize, maxChangeInArea, maxChangeInWidth, maxChangeInHeight, maxAngleBetweenChar, minNumberOfMatchCharNumber, topYOne, topYTwo, bottomYOne, bottomYTwo, self.oldCameraName))
            conn.commit()
            self.loadCameraDatabase()
            self.updateCameraPage.close()
            QMessageBox.information(self, 'Guncelleme Basarili!',
                                    "Kamera konfigürasyon güncellemesi başarı ile yapıldı!.",
                                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            if (results == None and resultsTwo == None):
                curs.execute("""UPDATE Cameras SET CameraName = ? , CameraIP = ? , CameraIPAddition = ? , Username = ? , Password = ? , 
                                ProtocolType = ? , MinPixelWidth = ? , MinPixelHeight = ? , MinPixelArea = ? , MinPixelRatio = ? , 
                                MaxPixelRatio = ? , MinDiagSize = ? , MaxDiagSize = ? , MaxChangeInArea = ? , MaxChangeInWidth = ? , 
                                MaxChangeInHeight = ? , MaxAngleBetweenChar = ? , MinNumberOfMatchCharNumber = ? , TopYOne = ? , 
                                TopYTwo = ? , BottomYOne = ? , BottomYTwo = ? WHERE CameraName = ?""",
                             (cameraName, cameraIP, cameraIPAddition, username, password, protocolType, minPixelWidth,
                              minPixelHeight, minPixelArea, minPixelRatio, maxPixelRatio, minDiagSize, maxDiagSize,
                              maxChangeInArea, maxChangeInWidth, maxChangeInHeight, maxAngleBetweenChar,
                              minNumberOfMatchCharNumber, topYOne, topYTwo, bottomYOne, bottomYTwo, self.oldCameraName))
                conn.commit()
                self.loadCameraDatabase()
                self.updateCameraPage.close()
                QMessageBox.information(self, 'Güncelleme Başarılı!',
                                        "Kamera konfigürasyon güncellemesi başarı ile yapıldı!.\n",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self, 'Güncelleme Hatası!',
                                    "Girilen kamera ismi sistemde mevcut!\n",
                                    QMessageBox.Ok, QMessageBox.Ok)


    def displayPhoto(self, img):
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

                    self.loadCameraDatabase()
                else:
                    self.loadCameraDatabase()
                self.show()

    def loadCameraDatabase(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        content = 'SELECT CameraName,CameraIP,CameraIPAddition,Username,Password, ProtocolType, MinPixelWidth ,MinPixelHeight,MinPixelArea,MinPixelRatio,MaxPixelRatio,MinDiagSize,MaxDiagSize,MaxChangeInArea,MaxChangeInWidth,MaxChangeInHeight,MaxAngleBetweenChar,MinNumberOfMatchCharNumber FROM Cameras'
        res = conn.execute(content)
        for row_index, row_data in enumerate(res):
            self.tableWidget.insertRow(row_index)
            for colm_index, colm_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
        self.labelCameraNumber.setText("Toplam Kamera Sayisi: " + str(self.tableWidget.rowCount()))
        return

    def TableClicked(self):
        self.buttonUpdateCamera.setEnabled(True)
        self.buttonDeleteCamera.setEnabled(True)

##############################################################################################
class Fonts(QDialog,Fonts.Ui_Dialog):
    def __init__(self,parent=None):
        super(Fonts,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Fontlar')
        self.InitUi()

    def InitUi(self):
        self.buttonDeleteFont.clicked.connect(self.DeleteFont)
        self.buttonUseFont.clicked.connect(self.UseFont)
        self.tableWidget.itemClicked.connect(self.TableClicked)
        self.buttonUseFont.setEnabled(False)
        self.buttonDeleteFont.setEnabled(False)
        self.LoadFontDatabase()

    def DeleteFont(self):
        self.buttonUseFont.setEnabled(False)
        self.buttonDeleteFont.setEnabled(False)
        content = "SELECT * FROM Fonts"
        res = conn.execute(content)
        for row in enumerate(res):
            if row[0] == self.tableWidget.currentRow():
                data = row[1]
                fontName = data[1]
                buttonReply = QMessageBox.question(self, 'Font Silme İşlemi', str(fontName) +
                                                   " isimli fontu sistemden silmek istediğinize emin misiniz?",
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    curs.execute("DELETE FROM Fonts WHERE FontName=?", (fontName,))
                    conn.commit()
                    shutil.rmtree("./Fonts/" + str(fontName),ignore_errors=True)
                    self.LoadFontDatabase()
                else:
                    self.LoadFontDatabase()
                self.show()

    def UseFont(self):
        self.buttonUseFont.setEnabled(False)
        self.buttonDeleteFont.setEnabled(False)

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
        self.setWindowTitle('Font Ekle')

##############################################################################################
class AddCamera(QDialog,AddCamera.Ui_Dialog):
    def __init__(self,parent=None):
        super(AddCamera,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Kamera Ekle')

##############################################################################################
class UpdateCamera(QDialog,UpdateCamera.Ui_Dialog):
    def __init__(self,parent=None):
        super(UpdateCamera,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Kamera Bilgilerini Güncelle')

##############################################################################################
class Char(QDialog,Char.Ui_Dialog):
    def __init__(self,parent=None):
        super(Char,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Harf Giriş Ekranı')

def main():
    app = QApplication([])
    win = MainWithGui()
    win.setWindowTitle('Vagon Plaka Takip')
    app.exec_()

main()
