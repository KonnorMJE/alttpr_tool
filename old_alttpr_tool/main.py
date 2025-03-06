import logging
import os

from config import EXE_DIR, LOG_LEVEL

logging.basicConfig(filename=os.path.join(EXE_DIR, 'log_file.log'), level=getattr(logging, LOG_LEVEL.upper()), format='%(asctime)s:%(levelname)s:%(message)s')
logging.debug("Starting application")
from gui.app import App


if __name__ == "__main__":
    app = App()
    app.mainloop()