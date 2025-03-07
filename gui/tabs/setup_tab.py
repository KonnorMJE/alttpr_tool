from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QCheckBox, QGroupBox, QGridLayout,
                            QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
import logging
import os
import shutil
from pathlib import Path

from alttpr_tool.config import Config
from alttpr_tool.database.operations import DatabaseOperations

class SetupTab(QWidget):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.db = DatabaseOperations()
        self.setup_ui()  # Call setup_ui in __init__
        self.refresh_data()  # Initial data load
        
    def setup_ui(self):
        """Initialize the UI components."""
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
        self.download_entry = QLineEdit()
        self.download_entry.setToolTip("Enter or browse for the download directory path")
        download_button = QPushButton("Browse...")
        download_button.setToolTip("Select a folder for downloads")
        download_button.clicked.connect(self.set_download_path)
        download_layout.addWidget(self.download_entry)
        download_layout.addWidget(download_button)
        paths_layout.addLayout(download_layout, 0, 1)

        # MSU Master Path
        msu_label = QLabel("MSU Master Folder:")
        msu_label.setToolTip("Directory containing all your MSU pack files")
        paths_layout.addWidget(msu_label, 1, 0)
        
        msu_layout = QHBoxLayout()
        self.msu_entry = QLineEdit()
        self.msu_entry.setToolTip("Enter or browse for the MSU packs directory")
        msu_button = QPushButton("Browse...")
        msu_button.setToolTip("Select your MSU packs folder")
        msu_button.clicked.connect(self.set_msu_path)
        msu_layout.addWidget(self.msu_entry)
        msu_layout.addWidget(msu_button)
        paths_layout.addLayout(msu_layout, 1, 1)

        # Tracker Path
        tracker_label = QLabel("Tracker Application:")
        tracker_label.setToolTip("Path to your ALTTPR tracker executable")
        paths_layout.addWidget(tracker_label, 2, 0)
        
        tracker_layout = QHBoxLayout()
        self.tracker_entry = QLineEdit()
        self.tracker_entry.setToolTip("Enter or browse for your tracker application")
        tracker_button = QPushButton("Browse...")
        tracker_button.setToolTip("Select your tracker application")
        tracker_button.clicked.connect(self.set_tracker_path)
        tracker_layout.addWidget(self.tracker_entry)
        tracker_layout.addWidget(tracker_button)
        paths_layout.addLayout(tracker_layout, 2, 1)

        layout.addWidget(paths_group)

        # Options Group
        options_group = QGroupBox("Options")
        options_group.setToolTip("General application settings and preferences")
        options_layout = QVBoxLayout(options_group)
        
        self.dark_mode = QCheckBox("Enable Dark Mode")
        self.dark_mode.setToolTip("Switch between light and dark application themes")
        self.dark_mode.stateChanged.connect(self.on_dark_mode_changed)
        options_layout.addWidget(self.dark_mode)
        
        self.auto_run = QCheckBox("Auto-run game")
        self.auto_run.setToolTip("Automatically start the game when you launch a randomized game")
        self.auto_run.stateChanged.connect(self.on_auto_run_changed)
        options_layout.addWidget(self.auto_run)

        layout.addWidget(options_group)

        # Save Button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        
        layout.addStretch()

    def set_download_path(self):
        """Open file dialog to select download directory."""
        path = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if path:
            self.download_entry.setText(path)

    def set_msu_path(self):
        """Open file dialog to select MSU directory."""
        path = QFileDialog.getExistingDirectory(self, "Select MSU Directory")
        if path:
            self.msu_entry.setText(path)

    def set_tracker_path(self):
        """Open file dialog to select tracker application."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Tracker Application",
            "",
            "Executable files (*.exe);;All files (*.*)"
        )
        if path:
            self.tracker_entry.setText(path)

    def on_dark_mode_changed(self, state):
        """Handle dark mode toggle."""
        # You'll need to implement the actual theme switching logic
        logging.info(f"Dark mode changed to: {state}")

    def on_auto_run_changed(self, state):
        """Handle auto-run toggle."""
        logging.info(f"Auto-run changed to: {state}")

    def is_default_or_nonexistent_path(self, path):
        """Check if path is default or doesn't exist."""
        if not path or "CHANGEME" in path or not os.path.exists(path):
            return True
        return False

    def save_settings(self):
        """Save all settings to database."""
        download_path = self.download_entry.text()
        msu_path = self.msu_entry.text()
        tracker_path = self.tracker_entry.text()
        
        if self.is_default_or_nonexistent_path(download_path):
            QMessageBox.critical(self, "Error", "Please input a valid Download Directory")
            return
        elif self.is_default_or_nonexistent_path(msu_path):
            QMessageBox.critical(self, "Error", "Please input a valid MSU Directory")
            return
            
        try:
            # Remove default directory if it exists
            if os.path.exists(os.path.join(self.config.BASE_DIR, 'CHANGEME')):
                shutil.rmtree(os.path.join(self.config.BASE_DIR, 'CHANGEME'))
                
            # Save settings to database
            self.db.save_settings_to_db(
                download_path,
                msu_path,
                tracker_path,
                self.dark_mode.isChecked(),
                self.auto_run.isChecked()
            )
            
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            logging.info("Settings saved successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
            logging.error(f"Error saving settings: {e}")

    def refresh_data(self):
        """Refresh all data and update UI elements."""
        settings = self.db.get_user_settings()
        if settings:
            self.download_entry.setText(settings.get("download_dir", ""))
            self.msu_entry.setText(settings.get("msu_master_dir", ""))
            self.tracker_entry.setText(settings.get("tracker_path", ""))
            self.dark_mode.setChecked(settings.get("dark_mode", False))
            self.auto_run.setChecked(settings.get("auto_run", False))