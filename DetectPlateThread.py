import imutils
from imutils.video import VideoStream
import imutils
import threading
import DetectChars
import datetime
import sqlite3
import DetectPlates
import cv2
import os
import time
import multiprocessing
import requests
from pythonping import ping

conn = sqlite3.connect('PlateDetectionDB.db', check_same_thread=False)
curs = conn.cursor()
path = os.getcwd() + "\\"
path = str(path)


def GetPing(ip):
    response = ping(ip, size=32, count=1)
    if(str(response)[0:7]=="Request"):
        return False
    else:
        return True

class camThread(threading.Thread):
    def __init__(self, cameraName):
        threading.Thread.__init__(self)
        self.cameraName = cameraName
        self.frameStatus = True
        self.image = None
        self.capture = None
        self.frameSize = (640, 480)
        searchall = curs.execute("""SELECT CameraIP, CameraIPAddition, Username, Password, ProtocolType,TopYOne, TopYTwo,
        BottomYOne, BottomYTwo FROM Cameras WHERE CameraName = ? """,(self.cameraName,))
        rows = searchall.fetchall()
        for row in rows:
            self.cameraIP = str(row[0])
            self.cameraIPAddition = str(row[1])
            self.username = str(row[2])
            self.password = str(row [3])
            self.protocolType = str(row[4])
            self.topYOne = int(row[5])
            self.topYTwo = int(row[6])
            self.bottomYOne = int(row[7])
            self.bottomYTwo = int(row[8])
        if (self.username != "" and self.password != ""):
            self.ip = self.protocolType + "://" + self.username + ":" + self.password + "@" + self.cameraIP + "/" + self.cameraIPAddition
        else:
            self.ip = self.protocolType + "://" + self.cameraIP + "/" + self.cameraIPAddition
        if (GetPing(self.cameraIP)):
            self.capture = VideoStream(src=self.ip, resolution=self.frameSize)
            self.capture.start()
        else:
            self.frameStatus = False
        self.stopped = False
        self.checkTop = 0
        self.checkBottom = 0
        self.checkPlateBottom = None
        self.checkPlateTop = None

    def run(self):
        while True:
            startTime = int(time.time())
            ThreadStatus = open("ThreadStatus.txt", "r")
            if (self.frameStatus == False):
                break
            if (str(ThreadStatus.readline()) == "False"):
                break
            self.image= self.capture.read()
            try:
                plateinfo = open("PlateInfo.txt", "r")
                line = str(plateinfo.readline())
                counts = line.split(",")
                topCharCount = int(counts[0])
                topMinCharCount = int(counts[1])
                bottomCharCount = int(counts[2])
                bottomMinCharCount = int(counts[3])
                controlCount = int(counts[4])
            except:
                topCharCount = 8
                topMinCharCount = 5
                bottomCharCount = 12
                bottomMinCharCount = 10
                controlCount = 5

            imgtop = self.image[self.topYOne:self.topYTwo, 0:640]
            imgbottom = self.image[self.bottomYOne:self.bottomYTwo, 0:640]

            listOfPossiblePlatesTop = DetectPlates.detectPlatesInScene(imgtop, 2)  # Plakaları tespit et
            listOfPossiblePlatesBottom = DetectPlates.detectPlatesInScene(imgbottom, 1)


            if (len(listOfPossiblePlatesTop) != 0):
                # Eğer program buraya geldiyse en azından bir plaka okunmuştur
                # Olası plakaların listesini DESCENDING sıralamasına göre sırala (Çok karakterden az karaktere)
                listOfPossiblePlatesTop = DetectChars.detectCharsInPlates(listOfPossiblePlatesTop, 2,
                                                                          self.cameraName)
                listOfPossiblePlatesTop.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
                licPlateTop = listOfPossiblePlatesTop[0]
                if (len(licPlateTop.strChars) >= topMinCharCount):
                    self.AddLogDatabase(licPlateTop.strChars)
                if (len(licPlateTop.strChars) == topCharCount):
                    if (self.checkPlateTop == licPlateTop.strChars):
                        self.checkTop += 1
                    else:
                        self.checkTop = 0
                    if (self.checkTop == controlCount):
                        self.AddPlateDatabase(licPlateTop.strChars, licPlateTop.imgThresh)
                    self.checkPlateTop = licPlateTop.strChars
            if (len(listOfPossiblePlatesBottom) != 0):
                listOfPossiblePlatesBottom = DetectChars.detectCharsInPlates(listOfPossiblePlatesBottom, 1,
                                                                             self.cameraName)
                listOfPossiblePlatesBottom.sort(key=lambda possiblePlate: len(possiblePlate.strChars),
                                                reverse=True)
                # Tanınmış karakterlere sahip plakanın (dize uzunluğu azalan şekilde ilk plaka) gerçek olduğunu varsay
                licPlateBottom = listOfPossiblePlatesBottom[0]
                if (len(licPlateBottom.strChars) >= bottomMinCharCount):
                    self.AddLogDatabase(licPlateBottom.strChars)
                if (len(licPlateBottom.strChars) == bottomCharCount):
                    if (self.checkPlateBottom == licPlateBottom.strChars):
                        self.checkBottom += 1
                    else:
                        self.checkBottom = 0
                    if (self.checkBottom == controlCount):
                        self.AddPlateDatabase(licPlateBottom.strChars, licPlateBottom.imgThresh)
                    self.checkPlateBottom = licPlateBottom.strChars
            lastTime = int(time.time())
            if(startTime==lastTime):
                time.sleep(1)

    def getDateAndTime(self):
        an = datetime.datetime.now()
        second = int(an.second)
        hour = int(an.hour)
        date = str(an.day) + "." + str(an.month) + "." + str(an.year)
        time = str(an.hour) + ":" + str(an.minute) + ":" + str(an.second)
        return date, time

    def AddLogDatabase(self,plate):
        date, time = self.getDateAndTime()
        curs.execute("INSERT INTO Log (Plate,Date,Time,Camera) VALUES(?,?,?,?)",
                     (plate, date, time, self.cameraName))
        conn.commit()

    def AddPlateDatabase(self, plate, imgThresh):
        date, time = self.getDateAndTime()
        sent = "Hayır"
        searchall = curs.execute('SELECT Plate FROM Plates WHERE Plate = ? AND Camera =?', (plate, self.cameraName,))
        rows = searchall.fetchall()
        i = 0
        if (rows != None):
            for row in rows:
                i = i + 1
        if (i == 0):
            curs.execute("INSERT INTO Plates (Plate,Date,Time,Camera,Sent) VALUES(?,?,?,?,?)",
                         (plate, date, time, self.cameraName, sent))
            conn.commit()




