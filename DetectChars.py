import os
import cv2
import numpy as np
import math
import random
import Preprocess
import PossibleChar

kNearest = cv2.ml.KNearest_create()
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

#checkIfPossibleChar için sabitler, bu yalnızca olası bir karakteri kontrol eder (başka bir karakterle karşılaştırılmaz)
"""MIN_PIXEL_WIDTH = 8
MIN_PIXEL_HEIGHT = 32
MIN_PIXEL_AREA = 80
MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0"""
MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 4
MIN_PIXEL_AREA = 40
MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0

# İki karakterin karşılaştırılması için sabitler
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 8.0
#MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0 en iyisi

MAX_CHANGE_IN_AREA = 0.9
MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2
MAX_ANGLE_BETWEEN_CHARS = 10.0
#MAX_ANGLE_BETWEEN_CHARS = 10.0 #en iyisi, 12 yapılabilir


# Diğer sabitlemeler
MIN_NUMBER_OF_MATCHING_CHARS = 3

RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100

def loadKNNDataAndTrainKNN():
    allContoursWithData = []                # Boş liste tanımlama
    validContoursWithData = []              # Boş liste tanımalama
    try:
        npaClassifications = np.loadtxt("classifications.txt", np.float32)     # Eğitim sınıflandırmalarından okuma
        npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)  # Eğitim resimlerini okuma
    except:                                                                    # Eğer dosya açılamadıysa
        pass
    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       # Numpy dizisini 1 boyutlu hale getirme
    kNearest.setDefaultK(1)                                                             # K'yı varsayılan olarak 1 yapma
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)           # KNN nesnelerini eğitme

    return True  #Eğer buraya gelirsek eğitim başarılı olmuştur

###################################################################################################
def detectCharsInPlates(listOfPossiblePlates,type):
    intPlateCounter = 0
    imgContours = None
    contours = []

    if len(listOfPossiblePlates) == 0:          # Olası plakaların listesi boşsa
        return listOfPossiblePlates             # listeyi döndür

    # Eğer bu noktaya geldiyse plakalar listesinde en az bir plaka olduğundan emin olabiliriz
    for possiblePlate in listOfPossiblePlates:          # Her olası plaka için for döngüsü
        possiblePlate.imgGrayscale, possiblePlate.imgThresh = Preprocess.preprocess(possiblePlate.imgPlate, type)     # Gri tonlamalı ve threshold görüntüler elde etmek için önişlem
        # Daha kolay görüntüleme ve karakter algılama için plaka görüntüsünün boyutunu arttırır
        #possiblePlate.imgThresh = cv2.resize(possiblePlate.imgThresh, (0, 0), fx = 1.0, fy = 1.0)
        #Gri alanları gidermek için tekrar threshold
        thresholdValue, possiblePlate.imgThresh = cv2.threshold(possiblePlate.imgThresh, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Plakadaki tüm olası karakterleri bulma
        # Bu işlev ilk önce tüm konturları bulur, ardından sadece karakter alabilecek kontürleri içerir (diğer karakterlerle karşılaştırmadan)
        listOfPossibleCharsInPlate = findPossibleCharsInPlate(possiblePlate.imgGrayscale, possiblePlate.imgThresh)

        # Olası tüm karakterlerin bir listesi verildiğinde, plaka içindeki eşleşen karakter gruplarını bulur
        listOfListsOfMatchingCharsInPlate = findListOfListsOfMatchingChars(listOfPossibleCharsInPlate)

        if (len(listOfListsOfMatchingCharsInPlate) == 0):   #Plakada eşleşen karakter grubu bulunamazsa
            possiblePlate.strChars = ""
            continue	#Loop için başa dön

        for i in range(0, len(listOfListsOfMatchingCharsInPlate)):  # Eşleşen karakterlerin her listesi ile
            listOfListsOfMatchingCharsInPlate[i].sort(key = lambda matchingChar: matchingChar.intCenterX)  # Karakterleri soldan sağa sırala
            listOfListsOfMatchingCharsInPlate[i] = removeInnerOverlappingChars(listOfListsOfMatchingCharsInPlate[i]) #üst üste binen karakterleri kaldır

        # Her olası plaka içerisinde, potansiyel eşleştirme karakterlerinin en uzun listesinin gerçek karakter listesi olduğunu varsay
        intLenOfLongestListOfChars = 0
        intIndexOfLongestListOfChars = 0

        # Eşleşen karakterlerin tüm vektörlerinde dolaş, en çok karaktere sahip olanın dizinini al
        for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
            if len(listOfListsOfMatchingCharsInPlate[i]) > intLenOfLongestListOfChars:
                intLenOfLongestListOfChars = len(listOfListsOfMatchingCharsInPlate[i])
                intIndexOfLongestListOfChars = i

        # Plaka içerisinde eşleşen en uzun karakter listesinin gerçek karakter listesi olduğunu varsayalım
        longestListOfMatchingCharsInPlate = listOfListsOfMatchingCharsInPlate[intIndexOfLongestListOfChars]
        possiblePlate.strChars = recognizeCharsInPlate(possiblePlate.imgThresh, longestListOfMatchingCharsInPlate)

    return listOfPossiblePlates

###################################################################################################
def findPossibleCharsInPlate(imgGrayscale, imgThresh):
    listOfPossibleChars = []                    
    contours = []
    imgThreshCopy = imgThresh.copy()

    # Plakadaki tüm konturları bul
    contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:    #her bir kontur için
        possibleChar = PossibleChar.PossibleChar(contour)

        if checkIfPossibleChar(possibleChar):        # Konturlar olası bir karakter ise, diğer karakterlerle karşılaştırılmaz (henüz)
            listOfPossibleChars.append(possibleChar) # Olası karakterlerin listesine ekle

    return listOfPossibleChars

###################################################################################################
def checkIfPossibleChar(possibleChar):
    # Bir karakter olup olmadığını görmek için kontur üzerinde kaba bir kontrol yapan (ilk geçiş) işlevidir
    # (Bir grubu aramak için henüz karakteri diğer karakterlerle karşılaştırmadık)
    if (possibleChar.intBoundingRectArea > MIN_PIXEL_AREA and
        possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH and possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
        MIN_ASPECT_RATIO < possibleChar.fltAspectRatio and possibleChar.fltAspectRatio < MAX_ASPECT_RATIO):
        return True
    else:
        return False

###################################################################################################
def findListOfListsOfMatchingChars(listOfPossibleChars):
    # Bu fonksiyonla mümkün olan tüm karakterlerle büyük bir listede başlıyoruz
    # Bu işlevin amacı, büyük bir karakter listesinin, eşleşen karakter listelerinin listesine yeniden düzenlenmesidir.
    # Bir eşleşme grubunda bulunamayan karakterlerin daha fazla dikkate alınması gerekmediğine dikkat edilmeli
    listOfListsOfMatchingChars = [] # bu dönüş değeri olacak

    for possibleChar in listOfPossibleChars:   # Tek bir büyük listedeki olası her karakter için
        listOfMatchingChars = findListOfMatchingChars(possibleChar, listOfPossibleChars)  # Mevcut listede yer alan büyük listedeki tüm karakterleri bul
        listOfMatchingChars.append(possibleChar)   # Ayrıca mevcut karakteri, eşleşen olası karakterler listesine ekle


        if len(listOfMatchingChars) < MIN_NUMBER_OF_MATCHING_CHARS:  # Mevcut olası eşleştirme karakter listesi olası bir plaka oluşturacak kadar uzun değilse
            continue                            # for döngüsünün en üstüne geri dönün ve bir sonraki karakterle tekrar deneyin, gerekli olmadığını unutmayın
                                                # Listeyi herhangi bir şekilde kaydetmek, muhtemel bir plaka olmak için yeterli değildir
        # Buraya gelirsek, mevcut liste testi eşleşen karakterlerin "grup" veya "küme" olarak geçti.
        listOfListsOfMatchingChars.append(listOfMatchingChars)      # bu yüzden eşleşen karakterlerin listesini listemize ekleyin
        listOfPossibleCharsWithCurrentMatchesRemoved = []

        # Eşleşen karakterlerin mevcut listesini büyük listeden kaldır ki aynı karakterleri iki kere kullanma
        # Orijinal büyük listeyi değiştirmek istemediğimizden bunun için yeni bir büyük liste yaptığınızdan emin ol
        listOfPossibleCharsWithCurrentMatchesRemoved = list(set(listOfPossibleChars) - set(listOfMatchingChars))
        recursiveListOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleCharsWithCurrentMatchesRemoved) # recursive çağrı
        for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars:        # Eşleşen karakterlerin her listesi için recursive çağrı
            listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)             # Orjinal eşleşen listelerin listesine, listemizi ekle
        break
    return listOfListsOfMatchingChars

###################################################################################################
def findListOfMatchingChars(possibleChar, listOfChars):
    # Bu fonksiyonun amacı, olası bir karakter ve olası bir karakter listesinin büyük bir listesidir,
    # Tüm olası karakterleri tek bir olası karakterin eşleşeceği büyük listede bul ve eşleşen karakterleri bir liste olarak döndür
    listOfMatchingChars = []   # Bu dönüş değeri olacak

    for possibleMatchingChar in listOfChars:        # Büyük listedeki her karakter için
        if possibleMatchingChar == possibleChar:    # Eşleşmeyi bulmaya çalıştığımız karakter, büyük listedeki karakterle tam olarak aynı karakter ise
                                                    # O zaman mevcut karakter dahil iki katına çıkacak olan b / c karşılaşmaları listesine dahil etmemeliyiz
            continue                                # Bu yüzden eşleşmeler listesine ekleme ve döngünün başına geri dön
        # Karakterlerin eşleşip eşleşmediğini görmek için işleri hesapla
        fltDistanceBetweenChars = distanceBetweenChars(possibleChar, possibleMatchingChar)

        fltAngleBetweenChars = angleBetweenChars(possibleChar, possibleMatchingChar)
        fltChangeInArea = float(abs(possibleMatchingChar.intBoundingRectArea - possibleChar.intBoundingRectArea)) / float(possibleChar.intBoundingRectArea)
        fltChangeInWidth = float(abs(possibleMatchingChar.intBoundingRectWidth - possibleChar.intBoundingRectWidth)) / float(possibleChar.intBoundingRectWidth)
        fltChangeInHeight = float(abs(possibleMatchingChar.intBoundingRectHeight - possibleChar.intBoundingRectHeight)) / float(possibleChar.intBoundingRectHeight)

        # Karakterlerin eşleşip eşleşmediğini kontrol et
        if (fltDistanceBetweenChars < (possibleChar.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and
            fltAngleBetweenChars < MAX_ANGLE_BETWEEN_CHARS and
            fltChangeInArea < MAX_CHANGE_IN_AREA and
            fltChangeInWidth < MAX_CHANGE_IN_WIDTH and
            fltChangeInHeight < MAX_CHANGE_IN_HEIGHT):

            listOfMatchingChars.append(possibleMatchingChar)  # Eğer karakterler eşleşirse, mevcut karakterleri eşleşen karakterlerin listesine ekle
    return listOfMatchingChars   #sonucu döndür

###################################################################################################
# İki karakter arasındaki mesafeyi hesaplamak için Pisagor teoremini kullan
def distanceBetweenChars(firstChar, secondChar):
    intX = abs(firstChar.intCenterX - secondChar.intCenterX)
    intY = abs(firstChar.intCenterY - secondChar.intCenterY)

    return math.sqrt((intX ** 2) + (intY ** 2))

###################################################################################################
# Karakterler arasındaki açıyı hesaplamak için temel trigonometri (SOH CAH TOA) kullan
def angleBetweenChars(firstChar, secondChar):
    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))
    if fltAdj != 0.0:   # merkez X konumları eşit olduğunda sıfıra bölmediğimizden emin ol, Python'da sıfıra bölme hata verir
        fltAngleInRad = math.atan(fltOpp / fltAdj)    # Sıfır değilse, açıyı hesapla
    else:
        fltAngleInRad = 1.5708 # bitişik sıfırsa, açı olarak kullan
    fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)   # derece cinsinden açı hesaplamak
    return fltAngleInDeg

###################################################################################################
# Üst üste binen iki karakterimiz varsa veya birbirinden ayrı karakter olması için birbirine yakınsak, içteki (küçük) karakter dizisini çıkartın,
# Bu, aynı karakter için iki kontür bulunursa, aynı karakterin iki kez eklenmesini önlemek içindir,
# Örneğin 'O' harfi için hem iç halka hem de dış halka kontür olarak bulunabilir, ancak sadece bir kez karakterin dahil edilmesi gerekir
def removeInnerOverlappingChars(listOfMatchingChars):
    listOfMatchingCharsWithInnerCharRemoved = list(listOfMatchingChars)  # bu dönüş değeri olacak
    for currentChar in listOfMatchingChars:
        for otherChar in listOfMatchingChars:
            if currentChar != otherChar:        # Mevcut karakterle diğer karakter aynı karakter değilse,
                                                # Eğer mevcut karakter ve diğer karakter neredeyse aynı yerde merkez noktalarına sahipse
                if distanceBetweenChars(currentChar, otherChar) < (currentChar.fltDiagonalSize * MIN_DIAG_SIZE_MULTIPLE_AWAY):
                    # Eğer buraya girersek üst üste binen karakterleri bulduk
                    # Daha sonra hangi char'in daha küçük olduğunu tespit edeceğiz, o zaman bu char daha önceki bir pasoda daha önce kaldırılmamışsa, onu kaldır
                    if currentChar.intBoundingRectArea < otherChar.intBoundingRectArea:   # Mevcut karakter diğer karakterlerden küçükse
                        if currentChar in listOfMatchingCharsWithInnerCharRemoved:        # Mevcut karakter önceki bir geçişte zaten kaldırılmadıysa
                            listOfMatchingCharsWithInnerCharRemoved.remove(currentChar)   # Geçerli karakteri kaldır
                    else:                                                                 # Aksi halde diğer karakter geçerli karakterden küçükse
                        if otherChar in listOfMatchingCharsWithInnerCharRemoved:
                            listOfMatchingCharsWithInnerCharRemoved.remove(otherChar)

    return listOfMatchingCharsWithInnerCharRemoved

###################################################################################################
# Gerçek karakter tanımayı uygulayacağımız yer
def recognizeCharsInPlate(imgThresh, listOfMatchingChars):
    strChars = ""    # Bu dönüş değeri olacaktır, plakadaki karakter sayısı
    height, width = imgThresh.shape
    imgThreshColor = np.zeros((height, width, 3), np.uint8)
    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)  # Karakterleri soldan sağa sırala
    cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR, imgThreshColor)                   # Üzerinde renkli konturlar çizebilmemiz için eşik görüntünün renkli sürüm
    for currentChar in listOfMatchingChars:                                       # Plakadaki her karakter için
        pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
        pt2 = ((currentChar.intBoundingRectX + currentChar.intBoundingRectWidth), (currentChar.intBoundingRectY + currentChar.intBoundingRectHeight))
        cv2.rectangle(imgThreshColor, pt1, pt2, SCALAR_GREEN, 2)           # Karakter etrafına yeşil kutu çiz
        # Karakteri kırp
        imgROI = imgThresh[currentChar.intBoundingRectY : currentChar.intBoundingRectY + currentChar.intBoundingRectHeight,
                           currentChar.intBoundingRectX : currentChar.intBoundingRectX + currentChar.intBoundingRectWidth]

        imgROIResized = cv2.resize(imgROI, (RESIZED_CHAR_IMAGE_WIDTH, RESIZED_CHAR_IMAGE_HEIGHT))          # Görüntüyü yeniden boyutlandır
        npaROIResized = imgROIResized.reshape((1, RESIZED_CHAR_IMAGE_WIDTH * RESIZED_CHAR_IMAGE_HEIGHT))   # Görüntüyü 1D numpy dizisine çevir
        npaROIResized = np.float32(npaROIResized)               # 1d numpy dizisi dizisini int'ten float'a çevir
        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)   # FindNearest ile arama yapabiliriz artık
        strCurrentChar = str(chr(int(npaResults[0][0])))            # Sonuçtan karakterleri al
        strChars = strChars + strCurrentChar                        # Geçerli karakterleri diziye ekle
    return strChars