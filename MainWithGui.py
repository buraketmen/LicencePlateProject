import os
import cv2
import datetime
import locale
import base64
#import urllib2
import numpy as np
import DetectChars
import DetectPlates
import PossiblePlate
from GUI import Ui_MainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem
import sqlite3

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

locale.setlocale(locale.LC_ALL, '')
conn = sqlite3.connect('PlakaDB.db')
curs = conn.cursor()
curs.execute("""
            CREATE TABLE IF NOT EXISTS Plates(
            Id INTEGER PRIMARY KEY,
            Plate TEXT,
            Date TEXT,
            Time TEXT)
            """)
curs.execute("DELETE FROM Plates")

class MainWithGui(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWithGui,self).__init__(parent)
        self.setupUi(self)
        self.capture = None
        self.croppedimage = None
        self.croppedimage2 = None
        self.checkPlateTop = None
        self.checkTop = 0
        self.checkPlateBottom = None
        self.checkBottom = 0
        try:
            self.backimage= cv2.imread('background.jpg')
        except:
            pass
        self.InitUi()

    def InitUi(self):
        self.show()
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


    def detectWebcam(self, status):
        if status:
            self.detectButton.setText('Plaka Tanımayı Durdur')
            self.plateEnabled = True

        else:
            self.detectButton.setText('Plaka Tanimayi Baslat')
            self.plateEnabled = False

    def startWebcam(self):
        try:

            #'rtsp://root:root@192.168.10.34/axis-media/media.amp'
            self.capture = cv2.VideoCapture(0)
            #self.capture = cv2.VideoCapture('rtsp://root:root@192.168.10.34/axis-media/media.amp')

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
        self.capture.release()
        if(self.plateEnabled != False):
            self.plateEnabled= False
            self.detectButton.toggle()
            self.detectButton.setText('Plaka Tanimayi Baslat')
        self.timer.stop()
        self.displayImage(self.backimage,1)
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
        ret, self.image = self.capture.read()
        if (self.plateEnabled):
            detectedImage = self.detectPlate(self.image)
            self.displayImage(detectedImage)
        else:
            self.displayImage(self.image)

    def detectPlate(self, img):
        imgtop = self.image[0:240, 0:640]
        imgbottom = self.image[240:480, 0:640]
        #imgtop = cv2.resize(imgtop, (0, 0), fx = 2.0, fy = 2.0)
        #imgbottom = cv2.resize(imgbottom,(0, 0), fx = 2.0, fy = 2.0)


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
                if (self.checkTop == 6):
                    self.Add2Database(licPlateTop.strChars, licPlateTop.imgPlate, licPlateTop.imgThresh, img)
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
                    if (self.checkBottom == 6):
                        self.Add2Database(licPlateBottom.strChars, licPlateBottom.imgPlate,
                                          licPlateBottom.imgThresh, img)
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


def main():
    app = QApplication([])
    win = MainWithGui()
    win.setWindowTitle('Vagon Plaka Takip')
    app.exec_()

main()

"""
                ptCenterOfTextAreaX = 0  # Metnin yazılacağı alanın merkezi olacak
                ptCenterOfTextAreaY = 0
                ptLowerLeftTextOriginX = 0  # Metnin yazılacağı alanın sol altında olacak
                ptLowerLeftTextOriginY = 0

                sceneHeight, sceneWidth, sceneNumChannels = img.shape
                plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape
                intFontFace = cv2.FONT_HERSHEY_SIMPLEX  # Yazı fontu
                fltFontScale = float(plateHeight) / 30.0  # Plaka alanının yüksekliğine göre temel font ölçeği
                intFontThickness = int(round(fltFontScale * 1.5))  # Yazı tipinin kalınlık-incelik ayarı
                textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale,
                                                 intFontThickness)  # getTextSize komutunu çağır

                # döndürülmüş kesiti merkez noktası, genişlik, yükseklik ve açısıyla aç
                ((intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight),
                 fltCorrectionAngleInDeg) = licPlate.rrLocationOfPlateInScene

                intPlateCenterX = int(intPlateCenterX)  # Merkezin tam sayı haline getir
                intPlateCenterY = int(intPlateCenterY)
                ptCenterOfTextAreaX = int(intPlateCenterX)  # Metin alanının yatay komutu plaka ile aynıdır
                if intPlateCenterY < (sceneHeight * 0.75):  # Eğer plaka görüntünün 3/4 ünden küçükse
                    ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))  # Plakayı alt kısma yaz
                else:
                    ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))  # Karakterleri üst kısma yaz
                textSizeWidth, textSizeHeight = textSize  # Metnin boyutunu ve yüksekliğini açma
                ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))  # metinin sol alt noktasını hesaplar
                ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))  # metin alanının merkezine, genişliğine ve yüksekliğine göre
                # Resmin üzerine yazı yaz
                cv2.putText(img, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY),
                            intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)
"""
