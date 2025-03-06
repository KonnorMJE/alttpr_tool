import os
import sys
from pathlib import Path

class Config:
    """Application configuration with OS-agnostic paths"""
    
    # Determine if the application is frozen (packaged)
    IS_FROZEN = getattr(sys, 'frozen', False)
    
    # Base directories
    if IS_FROZEN:
        BASE_DIR = Path(sys._MEIPASS)
        EXE_DIR = Path(sys.executable).parent
    else:
        BASE_DIR = Path(__file__).parent
        EXE_DIR = Path(__file__).parent

    # Application directories
    DATA_DIR = BASE_DIR / 'data'
    DATABASE_DIR = BASE_DIR / 'database'
    GUI_DIR = BASE_DIR / 'gui'
    PRESETS_DIR = BASE_DIR / 'presets'
    UTIL_DIR = BASE_DIR / 'utilities'
    TESTS_DIR = BASE_DIR / 'tests'
    
    # GUI assets
    ASSETS_DIR = GUI_DIR / 'assets'
    ICONS_DIR = ASSETS_DIR / 'icons'
    IMAGES_DIR = ASSETS_DIR / 'images'
    DARK_DIR = IMAGES_DIR / 'dark'
    LIGHT_DIR = IMAGES_DIR / 'light'
    
    # Google API Configurations
    CLIENT_SECRETS_FILE = DATA_DIR / 'client_secrets.json'
    TOKEN_PATH = DATA_DIR / 'token.pickle'
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/spreadsheets.readonly'
    ]
    FETCH_TIMEOUT_IN_SECONDS = 6 * 60 * 60  # 6 hours
    
    # URLs and Web Endpoints
    ALTTPR_WEBSITE_URL = 'https://alttpr.com/en'
    MSU_SHEET_ID = '1XRkR4Xy6S24UzYkYBAOv-VYWPKZIoUKgX04RbjF128Q'
    
    # App Configuration
    APP_WIDTH = 520
    APP_HEIGHT = 400
    
    @classmethod
    def read_log_level(cls):
        """Read log level from config file or create with default"""
        log_level_path = cls.EXE_DIR / 'log_level.txt'
        try:
            with open(log_level_path, 'r') as file:
                for line in file:
                    if line.startswith('LOG_LEVEL'):
                        _, log_level = line.split('=')
                        return log_level.strip()
        except FileNotFoundError:
            print(f"Log level config file not found. Creating file with default level")
            with open(log_level_path, 'w') as file:
                file.write("LOG_LEVEL = ERROR")
        return 'ERROR'
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.DATA_DIR,
            cls.DATABASE_DIR,
            cls.GUI_DIR,
            cls.PRESETS_DIR,
            cls.UTIL_DIR,
            cls.ASSETS_DIR,
            cls.ICONS_DIR,
            cls.IMAGES_DIR,
            cls.DARK_DIR,
            cls.LIGHT_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

# Initialize log level
LOG_LEVEL = Config.read_log_level()

# Ensure directories exist
Config.ensure_directories()
