from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QPushButton, QFrame, QGroupBox,
                            QListWidget, QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap
import re
import webbrowser
import logging
from pathlib import Path

from alttpr_tool.gui.widgets.moldorm_progress import MoldormProgress
from alttpr_tool.utilities.network import NetworkManager
from alttpr_tool.utilities.download_queue import DownloadQueue
from alttpr_tool.utilities.google_drive import GoogleDriveData
from alttpr_tool.utilities.google_sheets import GoogleSheetsData
from alttpr_tool.database.operations import DatabaseOperations


class MSUDownloadTab(QWidget):
    # Add signal for showing download report
    show_report_signal = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.network_manager = NetworkManager()
        self.db = DatabaseOperations()
        self.download_outcomes = {"success": [], "fail": [], "manual": []}
        self.download_queue = None  # Initialize as None
        
        # Connect signal to slot
        self.show_report_signal.connect(self._show_download_report)
        
        self.setup_ui()
        self.refresh_data()
        
    def setup_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Step 1: Selection Group
        selection_group = QGroupBox("Step 1: Select MSU Pack(s)")
        selection_layout = QVBoxLayout(selection_group)
        
        self.msu_dropdown = QComboBox()
        self.msu_dropdown.setMaxVisibleItems(15)  # Prevent excessive dropdown size
        add_button = QPushButton("Add to Queue")
        add_button.setFixedWidth(150)
        add_button.clicked.connect(self.add_msu)
        
        selection_layout.addWidget(self.msu_dropdown)
        selection_layout.addWidget(add_button)
        layout.addWidget(selection_group)

        # Step 2: Queue Group
        queue_group = QGroupBox("Step 2: Review Queue")
        queue_layout = QVBoxLayout(queue_group)
        
        self.msus_to_download = QListWidget()
        self.msus_to_download.setMinimumHeight(200)
        
        remove_button = QPushButton("Remove Selected")
        remove_button.setFixedWidth(150)
        remove_button.clicked.connect(self.remove_msu)
        
        queue_layout.addWidget(self.msus_to_download)
        queue_layout.addWidget(remove_button)
        layout.addWidget(queue_group)

        # Step 3: Download Group
        download_group = QGroupBox("Step 3: Start Download")
        download_layout = QVBoxLayout(download_group)
        
        self.progress_indicator = MoldormProgress()
        self.download_button = QPushButton("Start Download")
        self.download_button.setFixedWidth(150)
        self.download_button.clicked.connect(self.download_msus)
        
        download_layout.addWidget(self.download_button)
        download_layout.addWidget(self.progress_indicator)
        layout.addWidget(download_group)
        
        layout.addStretch()

    def refresh_data(self):
        """Refresh all data and update UI elements."""
        try:
            # Reset UI elements
            self.msu_dropdown.clear()
            self.msus_to_download.clear()
            self.progress_indicator.set_progress(0)
            self.download_outcomes = {"success": [], "fail": [], "manual": []}
            
            # Load fresh data
            if self.network_manager.check_internet_connection():
                self.sheets_data = GoogleSheetsData()
                if not self.sheets_data.get_msu_names():
                    self.sheets_data.get_all_data()
                self.msus_from_google_sheets = self.sheets_data.get_msu_names()
                if self.msus_from_google_sheets:
                    self.msu_dropdown.addItems(self.msus_from_google_sheets)
                    logging.info(f"Loaded {len(self.msus_from_google_sheets)} MSU packs")
                else:
                    logging.warning("No MSU packs found in Google Sheets")
        except Exception as e:
            logging.error(f"Error refreshing MSU data: {e}")
            QMessageBox.warning(self, "Error", "Failed to load MSU data")

    def add_msu(self):
        """Add selected MSU to download queue."""
        try:
            selection = self.msu_dropdown.currentText()
            if selection:
                self.msus_to_download.addItem(selection)
                file_id = self.extract_file_ids_from_links(
                    self.sheets_data.get_download_link(selection)
                )
                if not file_id:
                    item = self.msus_to_download.item(self.msus_to_download.count() - 1)
                    item.setBackground(Qt.GlobalColor.yellow)
                    self.download_outcomes["manual"].append(selection)
                    logging.info(f"Added {selection} as manual download")
        except Exception as e:
            logging.error(f"Error adding MSU: {e}")

    def remove_msu(self):
        """Remove selected MSU from download queue."""
        current_item = self.msus_to_download.currentItem()
        if current_item:
            msu_name = current_item.text()
            row = self.msus_to_download.row(current_item)
            self.msus_to_download.takeItem(row)
            
            # Remove from outcomes
            for outcome in self.download_outcomes.values():
                if msu_name in outcome:
                    outcome.remove(msu_name)

    def extract_file_ids_from_links(self, link):
        """Extract file ID from Google Drive link."""
        file_patterns = [
            r'^https?://drive\.google\.com/file/d/([^/]+)(/view\?.+)?',
            r'^https?://drive\.google\.com/open\?id=([^/]+)$'
        ]
        for pattern in file_patterns:
            match = re.match(pattern, link)
            if match:
                return match.group(1)
        return None

    def show_download_report(self):
        """Emit signal to show download report on main thread."""
        self.show_report_signal.emit(self.download_outcomes)

    def _show_download_report(self, outcomes):
        """Show download completion report (called on main thread)."""
        try:
            report = "Download Report\n\n"
            report += "Successful Downloads:\n" + "\n".join(outcomes["success"]) + "\n\n"
            report += "Failed Downloads:\n" + "\n".join(outcomes["fail"]) + "\n\n"
            report += "Manual Downloads:\n" + "\n".join(outcomes["manual"])

            msg = QMessageBox()
            msg.setWindowTitle("Download Report")
            msg.setText(report)
            msg.exec()
            
            if outcomes["manual"]:
                self.open_manual_download_links()
        except Exception as e:
            logging.error(f"Error showing download report: {e}")

    def open_manual_download_links(self):
        """Open manual download links in browser."""
        for msu_name in self.download_outcomes["manual"]:
            link = self.sheets_data.get_download_link(msu_name)
            webbrowser.open(link)

    def download_msus(self):
        """Start downloading selected MSUs."""
        try:
            def sanitize_file_names(file_name):
                return re.sub(r'[<>:"/\\|?*]', '-', file_name)

            self.progress_indicator.set_progress(0)
            selected_msu_names = [
                self.msus_to_download.item(i).text() 
                for i in range(self.msus_to_download.count())
            ]
            
            if not selected_msu_names:
                QMessageBox.warning(self, "Warning", "No MSUs selected for download")
                return

            # Create new download queue for each download session
            self.download_queue = DownloadQueue(all_downloads_complete_callback=self.show_download_report)
            self.download_outcomes = {"success": [], "fail": [], "manual": []}

            msu_data_list = self.sheets_data.get_msu_data(selected_msu_names)
            
            for i, msu_data in enumerate(msu_data_list):
                file_id = self.extract_file_ids_from_links(msu_data['Download'])
                if file_id:
                    try:
                        ext = '7z' if msu_data['Format'].lower() == "7-zip" else msu_data['Format'].lower()
                        file_name = sanitize_file_names(f"{msu_data['Pack Name']}.{ext}")
                        
                        settings = self.db.get_user_settings()
                        dl_destination = str(Path(settings['download_dir']) / file_name)
                        
                        def make_completion_callback(idx):
                            def callback(success, error=None):
                                try:
                                    item = self.msus_to_download.item(idx)
                                    if item:  # Check if item still exists
                                        color = Qt.GlobalColor.green if success else Qt.GlobalColor.red
                                        item.setBackground(color)
                                        msu_name = item.text()
                                        if success:
                                            self.download_outcomes["success"].append(msu_name)
                                        else:
                                            failure_reason = f'{msu_name}: {error}' if error else msu_name
                                            self.download_outcomes["fail"].append(failure_reason)
                                except Exception as e:
                                    logging.error(f"Error in completion callback: {e}")
                            return callback

                        self.download_queue.add_to_queue(
                            file_id, 
                            dl_destination,
                            GoogleDriveData.download_file,
                            self.progress_indicator.set_progress,
                            make_completion_callback(i)
                        )
                        logging.info(f"Added {msu_data['Pack Name']} to download queue")

                    except Exception as e:
                        logging.error(f"Error queueing {msu_data['Pack Name']}: {e}")
                        self.download_outcomes["fail"].append(f"{msu_data['Pack Name']}: {str(e)}")

            if self.download_outcomes["manual"] and len(self.download_outcomes["manual"]) == len(selected_msu_names):
                self.show_download_report()
                
        except Exception as e:
            logging.error(f"Error in download_msus: {e}")
            QMessageBox.critical(self, "Error", f"Download failed: {str(e)}") 