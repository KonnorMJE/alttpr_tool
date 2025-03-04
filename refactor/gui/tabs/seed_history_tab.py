from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableView, 
                           QHeaderView, QPushButton, QHBoxLayout,
                           QStyledItemDelegate)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from datetime import datetime

class ReadOnlyDelegate(QStyledItemDelegate):
    """Delegate to make certain columns read-only"""
    def createEditor(self, parent, option, index):
        return None

class SeedHistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create main layout
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
        
        # Add some sample data
        sample_data = [
            [datetime.now().strftime("%Y-%m-%d %H:%M"), 
             "Standard", 
             "Weekly Race Seed", 
             "https://alttpr.com/en/h/ABCDEF1234",
             "No",
             ""],
            [datetime.now().strftime("%Y-%m-%d %H:%M"), 
             "Keysanity", 
             "Practice Seed", 
             "https://alttpr.com/en/h/ZYXWVU5678",
             "Yes",
             "2:15:30"],
            [datetime.now().strftime("%Y-%m-%d %H:%M"), 
             "Entrance", 
             "Daily Challenge", 
             "https://alttpr.com/en/h/QWERTY9012",
             "No",
             ""],
        ]
        
        for row_data in sample_data:
            row_items = [QStandardItem(str(item)) for item in row_data]
            self.model.appendRow(row_items)
        
        # Make only Completed and Completion Time columns editable
        readonly_delegate = ReadOnlyDelegate(self)
        for col in range(4):  # First 4 columns are read-only
            self.table_view.setItemDelegateForColumn(col, readonly_delegate)
        
        # Set up column sizing
        self.table_view.setModel(self.model)
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Description column stretches
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        # Add buttons
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_data)
        
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)
        
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(export_button)
        button_layout.addStretch()
        
        # Add widgets to main layout
        layout.addWidget(self.table_view)
        layout.addLayout(button_layout)
        
    def refresh_data(self):
        """Refresh the table data (just prints for now)"""
        print("Refresh clicked")
        
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