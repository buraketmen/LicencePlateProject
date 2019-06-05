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
from pythonping import ping

conn = sqlite3.connect('PlateDetectionDB.db', check_same_thread=False)
curs = conn.cursor()
path = os.getcwd() + "\\"
path = str(path)

"""def GetResponse(ip):
    hostname = ip
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        return True
    else:
        return False"""

def GetPing(ip):
    response = ping(ip, size=5, count=2)
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
        frameSize = (640, 480)
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
            self.capture = VideoStream(src=self.ip, resolution=frameSize)
            self.image = self.capture.read()
        else:
            self.frameStatus = False
        if (self.image==None):
            self.frameStatus = False
        self.stopped = False
        self.checkTop = 0
        self.checkBottom = 0
        self.checkPlateBottom = None
        self.checkPlateTop = None

    def run(self):
        while True:
            if (self.frameStatus == False):
                break
            ThreadStatus = open("ThreadStatus.txt", "r")
            if (str(ThreadStatus.readline()) == "False"):
                break
            img = self.capture.read()
            if (len(img) != 0):
                imgtop = img[self.topYOne:self.topYTwo, 0:640]
                imgbottom = img[self.bottomYOne:self.bottomYTwo, 0:640]

                listOfPossiblePlatesBottom = DetectPlates.detectPlatesInScene(imgbottom, 1)
                listOfPossiblePlatesBottom = DetectChars.detectCharsInPlates(listOfPossiblePlatesBottom, 1,
                                                                             self.cameraName)
                listOfPossiblePlatesTop = DetectPlates.detectPlatesInScene(imgtop, 2)  # Plakaları tespit et
                listOfPossiblePlatesTop = DetectChars.detectCharsInPlates(listOfPossiblePlatesTop, 2,
                                                                          self.cameraName)
                if (len(listOfPossiblePlatesTop) != 0):
                    # Eğer program buraya geldiyse en azından bir plaka okunmuştur
                    # Olası plakaların listesini DESCENDING sıralamasına göre sırala (Çok karakterden az karaktere)
                    listOfPossiblePlatesTop.sort(key=lambda possiblePlate: len(possiblePlate.strChars),
                                                 reverse=True)
                    licPlateTop = listOfPossiblePlatesTop[0]
                    if (len(licPlateTop.strChars) > 6):
                        print(licPlateTop.strChars)
                    if (len(licPlateTop.strChars) == 8):
                        if (self.checkPlateTop == licPlateTop.strChars):
                            self.checkTop += 1
                        else:
                            self.checkTop = 0
                        if (self.checkTop == 5):
                            self.Add2Database(licPlateTop.strChars, licPlateTop.imgPlate, licPlateTop.imgThresh,
                                              imgtop)
                        self.checkPlateTop = licPlateTop.strChars
                    if (len(listOfPossiblePlatesBottom) != 0):
                        listOfPossiblePlatesBottom.sort(key=lambda possiblePlate: len(possiblePlate.strChars),
                                                        reverse=True)
                        # Tanınmış karakterlere sahip plakanın (dize uzunluğu azalan şekilde ilk plaka) gerçek olduğunu varsay
                        licPlateBottom = listOfPossiblePlatesBottom[0]
                        if (len(licPlateBottom.strChars) > 1):
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
                time.sleep(1)

    def Add2Database(self, plate, imgPlate, imgThresh, img):
        an = datetime.datetime.now()
        second = int(an.second)
        hour = int(an.hour)
        date = str(an.day) + "." + str(an.month) + "." + str(an.year)
        time = str(an.hour) + "." + str(an.minute) + "." + str(an.second)
        searchall = curs.execute('SELECT Plate FROM Plates WHERE Plate = ? AND Camera =?', (plate, self.cameraName,))
        rows = searchall.fetchall()
        i = 0
        if (rows != None):
            for row in rows:
                i = i + 1
        if (i == 0):
            try:
                cv2.imwrite(path + "PlatePhotos\\Thresh_{}_{}_{}.png".format(plate, date, time), imgThresh)
            except:
                pass
            curs.execute("INSERT INTO Plates (Plate,Date,Time,Camera) VALUES(?,?,?,?)",
                         (plate, date, time, self.cameraName))
            conn.commit()

