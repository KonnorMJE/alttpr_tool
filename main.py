import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from alttpr_tool.gui.main_window import MainWindow
from alttpr_tool.utilities.initialize_db import DatabaseInitializer

def main():
    db_initializer = DatabaseInitializer()
    db_initializer.initialize()
    
    if sys.platform == "darwin":  # macOS
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_MacDontSwapCtrlAndMeta)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 