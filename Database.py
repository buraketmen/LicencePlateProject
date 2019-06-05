import sqlite3

MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8
MIN_PIXEL_AREA = 60
MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.00
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 8.0
MAX_CHANGE_IN_AREA = 0.5
MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2
MAX_ANGLE_BETWEEN_CHARS = 12.0
MIN_NUMBER_OF_MATCHING_CHARS =8
RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100
def setDatabase():
    conn = sqlite3.connect('PlateDetectionDB.db')
    curs = conn.cursor()
    curs.execute("""
                CREATE TABLE IF NOT EXISTS Cameras(
                CameraId INTEGER PRIMARY KEY,
                CameraName TEXT,
                CameraIP TEXT,
                CameraIPAddition TEXT,
                Username TEXT,
                Password TEXT,
                ProtocolType TEXT,
                MinPixelWidth TEXT,
                MinPixelHeight TEXT,
                MinPixelArea TEXT,
                MinPixelRatio TEXT,
                MaxPixelRatio TEXT,
                MinDiagSize TEXT,
                MaxDiagSize TEXT,
                MaxChangeInArea TEXT,
                MaxChangeInWidth TEXT,
                MaxChangeInHeight TEXT,
                MaxAngleBetweenChar TEXT,
                MinNumberOfMatchCharNumber TEXT,
                TopYOne TEXT,
                TopYTwo TEXT,
                BottomYOne TEXT,
                BottomYTwo TEXT,
                CameraStatus TEXT)
                """)
    curs.execute("""
                CREATE TABLE IF NOT EXISTS Fonts(
                FontId INTEGER PRIMARY KEY,
                FontName TEXT,
                FontDate TEXT,
                FontFileDir TEXT,
                CharCountInFont TEXT)
                """)
    curs.execute("""
                CREATE TABLE IF NOT EXISTS Plates(
                PlateId INTEGER PRIMARY KEY,
                Plate TEXT,
                Date TEXT,
                Time TEXT,
                Camera TEXT)
                """)
    curs.execute("""
                CREATE TABLE IF NOT EXISTS Log(
                LogId INTEGER PRIMARY KEY,
                Plate TEXT,
                Date TEXT,
                Time TEXT
                Camera TEXT)
                """)

