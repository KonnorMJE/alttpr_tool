from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QCheckBox, QGridLayout, QGroupBox)

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