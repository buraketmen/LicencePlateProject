import cv2
import numpy as np
import math
import random
import Preprocess
import DetectChars
import PossiblePlate
import PossibleChar

PLATE_WIDTH_PADDING_FACTOR = 1.1
PLATE_HEIGHT_PADDING_FACTOR = 1.3
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

def detectPlatesInScene(imgOriginalScene,type):
    listOfPossiblePlates = []     # Dönüş değeri olacak
    height, width, numChannels = imgOriginalScene.shape
    imgGrayscaleScene = np.zeros((height, width, 1), np.uint8) #matris olusturma
    imgThreshScene = np.zeros((height, width, 1), np.uint8)
    imgContours = np.zeros((height, width, 3), np.uint8)
    cv2.destroyAllWindows()
    imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene,type)  # Gri tonlamalı ve eşikli görüntüler elde etmek için ön işlem
    # Sahnedeki tüm olası karakterleri bul
    # Bu işlev ilk önce tüm konturları bulur, ardından sadece karakter olabilecek kontürleri içerir (henüz diğer karakterlerle karşılaştırılmadan)
    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene)

    # Olası tüm karakterlerin bir listesi verildiğinde eşleşen karakter gruplarını bulun
    # Sonraki adımlarda, eşleşen her karakter grubu bir plaka olarak tanınmaya çalışacaktır
    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)

    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:             # Eşleşen karakter grubunun her biri için
        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)   # Plaka çıkarma girişimi
        if possiblePlate.imgPlate is not None:          # Eğer plaka bulunursa
            listOfPossiblePlates.append(possiblePlate)  # Olası plakalar listesine ekle
    return listOfPossiblePlates

def findPossibleCharsInScene(imgThresh):
    listOfPossibleChars = []  #Dönüş değeri olacak
    intCountOfPossibleChars = 0
    imgThreshCopy = imgThresh.copy()
    contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # Tüm kontürleri bul SIMPLE ile 4 kontür bulunur
    height, width = imgThresh.shape
    imgContours = np.zeros((height, width, 3), np.uint8)
    for i in range(0, len(contours)):    # Her bir kontür için
        possibleChar = PossibleChar.PossibleChar(contours[i])
        if DetectChars.checkIfPossibleChar(possibleChar):         # Kontur olası bir karakter ise, bunun diğer karakterlerle (henüz) karşılaştırılmadığını unutma
            intCountOfPossibleChars = intCountOfPossibleChars + 1 # Olası karakterlerin sayısını arttır
            listOfPossibleChars.append(possibleChar)              # Olası listeye ekle
    return listOfPossibleChars

def extractPlate(imgOriginal, listOfMatchingChars):
    possiblePlate = PossiblePlate.PossiblePlate()    # Dönüş değeri olacak

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)  # Karakterleri x konumuna göre sola veya sağa sıralayın

    # Plakanın merkez noktasını hesaplar
    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0

    ptPlateCenter = fltPlateCenterX, fltPlateCenterY
    # Plaka genişliği ve yüksekliğini hesaplar
    intPlateWidth = int((listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX + listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth - listOfMatchingChars[0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)
    intTotalOfCharHeights = 0
    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight

    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)
    intPlateHeight = int(fltAverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)
    # Plaka bölgesinin düzeltme açısını hesaplar
    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    fltHypotenuse = DetectChars.distanceBetweenChars(listOfMatchingChars[0], listOfMatchingChars[len(listOfMatchingChars) - 1])
    fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse)
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)

    # Paket bölgesinin merkez noktası, genişliği, yüksekliği ve plakanın döndürülmüş dikme elemanı değişkenine düzeltme açısı
    possiblePlate.rrLocationOfPlateInScene = ( tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg )

    # Son adımlar asıl dönüşü gerçekleştirmektir
    # Hesaplanan düzeltme açımız için rotasyon matrisini alın
    rotationMatrix = cv2.getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0)

    height, width, numChannels = imgOriginal.shape      # Orjinal görüntü genişliğini ve yüksekliğini açma
    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))  # Tüm resmi döndür
    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))
    possiblePlate.imgPlate = imgCropped         # Kırpılmış plaka görüntüsünü olası plakanın uygulanabilir üye değişkenine kopyala
    return possiblePlate