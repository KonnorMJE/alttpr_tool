import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                            QCheckBox, QGridLayout, QGroupBox, QTabWidget, QStackedWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

class SetupTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Paths Group
        paths_group = QGroupBox("File Locations")
        paths_group.setToolTip("Configure important file paths for the application")
        paths_layout = QGridLayout(paths_group)
        paths_layout.setSpacing(10)

        # Download Path
        download_label = QLabel("Download Path:")
        download_label.setToolTip("Location where generated seeds and MSU packs will be downloaded")
        paths_layout.addWidget(download_label, 0, 0)
        
        download_layout = QHBoxLayout()
        download_entry = QLineEdit()
        download_entry.setToolTip("Enter or browse for the download directory path")
        download_button = QPushButton("Browse...")
        download_button.setToolTip("Select a folder for downloads")
        download_button.clicked.connect(lambda: print("Download path button clicked"))
        download_layout.addWidget(download_entry)
        download_layout.addWidget(download_button)
        paths_layout.addLayout(download_layout, 0, 1)

        # MSU Master Path
        msu_label = QLabel("MSU Master Folder:")
        msu_label.setToolTip("Directory containing all your MSU pack files")
        paths_layout.addWidget(msu_label, 1, 0)
        
        msu_layout = QHBoxLayout()
        msu_entry = QLineEdit()
        msu_entry.setToolTip("Enter or browse for the MSU packs directory")
        msu_button = QPushButton("Browse...")
        msu_button.setToolTip("Select your MSU packs folder")
        msu_button.clicked.connect(lambda: print("MSU path button clicked"))
        msu_layout.addWidget(msu_entry)
        msu_layout.addWidget(msu_button)
        paths_layout.addLayout(msu_layout, 1, 1)

        # Tracker Path
        tracker_label = QLabel("Tracker Application:")
        tracker_label.setToolTip("Path to your ALTTPR tracker executable")
        paths_layout.addWidget(tracker_label, 2, 0)
        
        tracker_layout = QHBoxLayout()
        tracker_entry = QLineEdit()
        tracker_entry.setToolTip("Enter or browse for your tracker application")
        tracker_button = QPushButton("Browse...")
        tracker_button.setToolTip("Select your tracker application")
        tracker_button.clicked.connect(lambda: print("Tracker path button clicked"))
        tracker_layout.addWidget(tracker_entry)
        tracker_layout.addWidget(tracker_button)
        paths_layout.addLayout(tracker_layout, 2, 1)

        layout.addWidget(paths_group)

        # Options Group
        options_group = QGroupBox("Options")
        options_group.setToolTip("General application settings and preferences")
        options_layout = QVBoxLayout(options_group)
        
        dark_mode = QCheckBox("Enable Dark Mode")
        dark_mode.setToolTip("Switch between light and dark application themes")
        dark_mode.stateChanged.connect(lambda state: print(f"Dark mode: {state}"))
        options_layout.addWidget(dark_mode)
        
        auto_run = QCheckBox("Auto-run game")
        auto_run.setToolTip("Automatically start the game when you launch a randomized game")
        auto_run.stateChanged.connect(lambda state: print(f"Auto run: {state}"))
        options_layout.addWidget(auto_run)

        layout.addWidget(options_group)
        layout.addStretch()

class MainTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Main Window Content"))
        # Add your main window content here

class MSUDownloadTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("MSU Download Content"))
        # Add your MSU download content here

class GenerateSeedTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Generate Seed Content"))
        # Add your seed generation content here

class NavButton(QPushButton):
    def __init__(self, icon_path, text, tooltip=""):
        super().__init__()
        self.setCheckable(True)
        
        # Set icon and text
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(18, 18))  # Adjust size as needed
        
        self.setText(text)
        if tooltip:
            self.setToolTip(tooltip)
        
        # Style to align icon and text
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 15px 25px;
                border: none;
                border-radius: 0px;
                font-size: 14px;
                margin: 2px 0px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #3498db;
                border-left: 4px solid #2980b9;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALTTPR Tool")
        self.setMinimumSize(900, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: white;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Logo/Title area
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)
        
        # Optional: Add logo to title
        logo_label = QLabel()
        logo_label.setPixmap(QIcon("icons/logo.png").pixmap(QSize(32, 32)))
        title_layout.addWidget(logo_label)
        
        title = QLabel("ALTTPR Tool")
        title.setStyleSheet("font-size: 20px; padding: 25px; font-weight: bold;")
        title_layout.addWidget(title)
        sidebar_layout.addWidget(title_widget)

        # Main navigation
        nav_section = QLabel("NAVIGATION")
        nav_section.setStyleSheet("color: #95a5a6; padding: 15px 25px 5px 25px; font-size: 12px;")
        sidebar_layout.addWidget(nav_section)

        # Navigation buttons with icons
        self.nav_buttons = []
        pages = [
            ("", "Home", "Main dashboard", MainTab),
            ("icons/controller.png", "Generate", "Create new seeds", GenerateSeedTab),
            ("icons/music.png", "MSU Manager", "Download & manage packs", MSUDownloadTab),
        ]

        for icon_path, text, tooltip, page_class in pages:
            btn = NavButton(icon_path, text, tooltip)
            btn.clicked.connect(lambda checked, p=page_class: self.switch_page(p))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # Settings section at bottom
        settings_section = QLabel("SETTINGS")
        settings_section.setStyleSheet("color: #95a5a6; padding: 5px 25px; font-size: 12px;")
        sidebar_layout.addWidget(settings_section)

        settings_btn = NavButton("icons/settings.png", "Settings")
        settings_btn.setCheckable(True)
        settings_btn.clicked.connect(lambda: self.switch_page(SetupTab))
        self.nav_buttons.append(settings_btn)
        sidebar_layout.addWidget(settings_btn)

        # Version number
        version = QLabel("v1.0.0")
        version.setStyleSheet("color: #95a5a6; padding: 15px; font-size: 12px;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version)

        layout.addWidget(sidebar)

        # Content area
        self.stack = QStackedWidget()

        layout.addWidget(self.stack)

        # Add pages to stack
        for _, _, _, page_class in pages:
            self.stack.addWidget(page_class())
        self.stack.addWidget(SetupTab())

        # Set initial page
        self.nav_buttons[0].setChecked(True)
        self.stack.setCurrentIndex(0)

    def switch_page(self, page_class):
        # Uncheck all buttons except the clicked one
        for btn in self.nav_buttons:
            if btn.text() != self.sender().text():
                btn.setChecked(False)

        # Find and switch to the requested page
        for i in range(self.stack.count()):
            if isinstance(self.stack.widget(i), page_class):
                self.stack.setCurrentIndex(i)
                break

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()