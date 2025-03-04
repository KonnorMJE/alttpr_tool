from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QStackedWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from .widgets.nav_button import NavButton
from .tabs import MSUDownloadTab, GenerateSeedTab, SetupTab, MSUSelectTab, SeedHistoryTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALTTPR Tool")
        self.setMinimumSize(900, 600)
        self.setMaximumSize(900, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #90A959;  /* Matcha green */
                color: #f6edd9;  /* Light cream text */
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
        logo_label.setPixmap(QIcon("/Users/konnorkurilla/Documents/Development/Personal/alttpr_tool/refactor/gui/assets/icons/app-icon.ico").pixmap(QSize(32, 32)))
        title_layout.addWidget(logo_label)
        
        title = QLabel("ALTTPR Tool")
        title.setStyleSheet("font-size: 15px; padding: 10px; font-weight: bold;")
        title_layout.addWidget(title)
        sidebar_layout.addWidget(title_widget)

        # Main navigation
        nav_section = QLabel("NAVIGATION")
        nav_section.setStyleSheet("color: #F4F1DE; padding: 15px 25px 5px 25px; font-size: 12px; opacity: 0.8;")
        sidebar_layout.addWidget(nav_section)

        # Navigation buttons with icons
        self.nav_buttons = []
        pages = [
            ("icons/controller.png", "MSU Select", "Select MSU packs", MSUSelectTab),
            ("icons/controller.png", "Generate Seed", "Create new seeds", GenerateSeedTab),
            ("icons/music.png", "Download MSUs", "Download MSU packs", MSUDownloadTab),
            ("icons/history.png", "Seed History", "View seed history", SeedHistoryTab),
        ]

        for icon_path, text, tooltip, page_class in pages:
            btn = NavButton(icon_path, text, tooltip)
            btn.clicked.connect(lambda checked, p=page_class: self.switch_page(p))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # Settings section at bottom
        settings_section = QLabel("SETTINGS")
        settings_section.setStyleSheet("color: #F4F1DE; padding: 5px 25px; font-size: 12px; opacity: 0.8;")
        sidebar_layout.addWidget(settings_section)

        settings_btn = NavButton("icons/settings.png", "Settings")
        settings_btn.setCheckable(True)
        settings_btn.clicked.connect(lambda: self.switch_page(SetupTab))
        self.nav_buttons.append(settings_btn)
        sidebar_layout.addWidget(settings_btn)

        # Version number
        version = QLabel("v1.0.0")
        version.setStyleSheet("color: #F4F1DE; padding: 15px; font-size: 12px; opacity: 0.7;")
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