from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableView, 
                           QHeaderView, QPushButton, QHBoxLayout,
                           QStyledItemDelegate)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from datetime import datetime
import logging
from PyQt6.QtWidgets import QMessageBox

class ReadOnlyDelegate(QStyledItemDelegate):
    """Delegate to make certain columns read-only"""
    def createEditor(self, parent, option, index):
        return None

class SeedHistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.refresh_data()
        
    def setup_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # Create the table view
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setAlternatingRowColors(True)
        
        # Set up the model with headers
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "Date", "Seed Type", "Description", "Permalink", 
            "Completed", "Completion Time"
        ])
        
        # Make only Completed and Completion Time columns editable
        readonly_delegate = ReadOnlyDelegate(self)
        for col in range(4):  # First 4 columns are read-only
            self.table_view.setItemDelegateForColumn(col, readonly_delegate)
        
        # Set up column sizing
        self.table_view.setModel(self.model)
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_data)
        
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)
        
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(export_button)
        button_layout.addStretch()
        
        layout.addWidget(self.table_view)
        layout.addLayout(button_layout)

    def refresh_data(self):
        """Refresh all data and update UI elements."""
        try:
            # Clear existing data
            self.model.removeRows(0, self.model.rowCount())
            
            # Add fresh data (replace with your actual data source)
            sample_data = [
                [datetime.now().strftime("%Y-%m-%d %H:%M"), 
                 "Standard", 
                 "Weekly Race Seed", 
                 "https://alttpr.com/en/h/ABCDEF1234",
                 "No",
                 ""],
                # ... more data ...
            ]
            
            for row_data in sample_data:
                row_items = [QStandardItem(str(item)) for item in row_data]
                self.model.appendRow(row_items)
                
            logging.info("Refreshed seed history data")
            
        except Exception as e:
            logging.error(f"Error refreshing seed history: {e}")
            QMessageBox.warning(self, "Error", "Failed to refresh seed history")

    def export_to_csv(self):
        """Export the table data to CSV (just prints for now)"""
        print("Export clicked")
        
    def add_new_seed(self, seed_type, description, permalink):
        """Add a new seed to the history"""
        row_data = [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            seed_type,
            description,
            permalink,
            "No",
            ""
        ]
        row_items = [QStandardItem(str(item)) for item in row_data]
        self.model.appendRow(row_items)