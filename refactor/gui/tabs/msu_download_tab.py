from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QPushButton, QFrame, QGroupBox,
                            QListWidget, QProgressBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
import random
import os
from ..widgets.moldorm_progress import MoldormProgress

class MSUDownloadTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Step 1: Selection Group
        selection_group = QGroupBox("Step 1: Select MSU Pack(s)")
        selection_group.setToolTip("Choose an MSU pack to add to the download queue")
        selection_layout = QVBoxLayout(selection_group)
        selection_layout.setSpacing(10)
        
        self.msu_dropdown = QComboBox()
        self.msu_dropdown.addItems(["MSU Pack 1", "MSU Pack 2", "MSU Pack 3"])
        
        add_button = QPushButton("Add to Queue")
        add_button.setFixedWidth(150)
        add_button.clicked.connect(self.add_to_queue)
        
        selection_layout.addWidget(self.msu_dropdown)
        selection_layout.addWidget(add_button)
        layout.addWidget(selection_group)

        # Step 2: Queue Group
        queue_group = QGroupBox("Step 2: Review Queue")
        queue_group.setToolTip("Review and manage MSU packs to be downloaded")
        queue_layout = QVBoxLayout(queue_group)
        queue_layout.setSpacing(10)
        
        self.msus_to_download = QListWidget()
        self.msus_to_download.setMinimumHeight(200)
        
        remove_button = QPushButton("Remove Selected")
        remove_button.setFixedWidth(150)
        remove_button.clicked.connect(self.remove_from_queue)
        
        queue_layout.addWidget(self.msus_to_download)
        queue_layout.addWidget(remove_button)
        layout.addWidget(queue_group)

        # Step 3: Download Group
        download_group = QGroupBox("Step 3: Start Download")
        download_group.setToolTip("Start download and view progress")
        download_layout = QVBoxLayout(download_group)
        download_layout.setSpacing(10)
        
        # Create a container widget for the progress indicator
        progress_container = QWidget()
        progress_container.setMinimumHeight(100)  # Ensure enough height
        progress_container_layout = QVBoxLayout(progress_container)
        progress_container_layout.setContentsMargins(10, 10, 10, 10)
        
        self.progress_indicator = MoldormProgress()
        progress_container_layout.addWidget(self.progress_indicator)
        
        self.download_button = QPushButton("Start Download")
        self.download_button.setFixedWidth(150)
        self.download_button.clicked.connect(self.simulate_download)
        
        download_layout.addWidget(self.download_button)
        download_layout.addWidget(progress_container)
        layout.addWidget(download_group)
        
        layout.addStretch()

        # Setup timer for simulated download
        self.progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        
    def add_to_queue(self):
        """Add selected MSU to download queue"""
        current_msu = self.msu_dropdown.currentText()
        self.msus_to_download.addItem(current_msu)

    def remove_from_queue(self):
        """Remove selected MSU from download queue"""
        current_item = self.msus_to_download.currentItem()
        if current_item:
            self.msus_to_download.takeItem(self.msus_to_download.row(current_item))

    def simulate_download(self):
        """Start simulated download"""
        if self.msus_to_download.count() == 0:
            return
            
        self.progress = 0
        self.download_button.setEnabled(False)
        self.progress_indicator.set_progress(0)
        self.timer.start(100)  # Update every 100ms

    def update_progress(self):
        """Update progress for simulation"""
        self.progress += 2  # Increment by 2% each time
        self.progress_indicator.set_progress(self.progress)
        
        if self.progress >= 100:
            self.timer.stop()
            self.download_button.setEnabled(True)
            self.progress = 0 