import os
import sys

# Directories
# BASE_DIR
# ├── data
# ├── database
# └── gui
#     └── assets
#         ├── icons
#         └── images
#             ├── dark
#             └── light
# ├── tests
# ├── utilities

def read_log_level():
    log_level_path = os.path.join(EXE_DIR, 'log_level.txt')
    try:
        with open(log_level_path, 'r') as file:
            for line in file:
                if line.startswith('LOG_LEVEL'):
                    _, log_level = line.split('=')
                    return log_level.strip()
    except FileNotFoundError:
        print(f"Log level config file not found. Creating file with default level")
        with open(log_level_path, 'w') as file:
            file.write(f"LOG_LEVEL = ERROR")
    return 'ERROR'

# Determine if the application is frozen (packaged)
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    EXE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE_DIR = os.path.dirname(os.path.abspath(__file__))


# Directories
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
GUI_DIR = os.path.join(BASE_DIR, 'gui')
PRESETS_DIR = os.path.join(BASE_DIR, 'presets')
UTIL_DIR = os.path.join(BASE_DIR, 'utilities')



# GUI subdirectories
ASSETS_DIR = os.path.join(GUI_DIR, 'assets')
ICONS_DIR = os.path.join(ASSETS_DIR, 'icons')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')

# Image theme subdirectories
DARK_DIR = os.path.join(IMAGES_DIR, 'dark')
LIGHT_DIR = os.path.join(IMAGES_DIR, 'light')

TESTS_DIR = os.path.join(BASE_DIR, 'tests')
UTILITIES_DIR = os.path.join(BASE_DIR, 'utilities')

DOWNLOAD_DIR = os.path.expanduser('~\Downloads')
MSU_MASTER_DIR = os.path.join('D:\ALTTPR', 'MSUs')

# Google API Configurations
GOOGLE_CREDENTIALS_PATH = os.path.join(DATA_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(DATA_DIR, 'token.pickle')
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/drive.readonly',
                 'https://www.googleapis.com/auth/spreadsheets.readonly'
                 ]
FETCH_TIMEOUT_IN_SECONDS = 6 * 60 * 60 # 6 hours

# URLs and Web Endpoints
ALTTPR_WEBSITE_URL = 'https://alttpr.com/en'
MSU_SHEET_ID = '1XRkR4Xy6S24UzYkYBAOv-VYWPKZIoUKgX04RbjF128Q'

# App Configuration
APP_WIDTH = 520
APP_HEIGHT = 400 # nice
BUTTON_WIDTH = 10

# Log Level
LOG_LEVEL = read_log_level()
