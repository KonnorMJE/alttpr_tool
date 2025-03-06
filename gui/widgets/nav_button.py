from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

class NavButton(QPushButton):
    def __init__(self, icon_path, text, tooltip=""):
        super().__init__()
        self.setCheckable(True)
        
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(18, 18))
        
        self.setText(text)
        if tooltip:
            self.setToolTip(tooltip)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #f6edd9;
                text-align: left;
                padding: 10px 25px;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #89966a;  /* Darker matcha */
            }
            QPushButton:checked {
                background-color: #5c7528;  /* Even darker matcha */
                border-left: 4px solid #F4F1DE;
            }
        """) 