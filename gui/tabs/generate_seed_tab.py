import logging
import os
import webbrowser
import yaml

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QPushButton, QFrame, QGroupBox,
                            QCheckBox)
from PyQt6.QtCore import Qt

from alttpr_tool.config import Config 
from alttpr_tool.utilities.seed_generator import get_yaml_presets, main_generate


class GenerateSeedTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        logging.info("Generate Seed Tab initialized") 

        self.preset_names = get_yaml_presets()  # Get list of presets from the presets dir

        # Generate Seed Group 
        mode_group = QGroupBox("Generate New Seed")
        mode_group.setToolTip("Select a game mode to generate your seed")
        mode_layout = QVBoxLayout(mode_group)
        mode_layout.setSpacing(10)

        # Game Mode Dropdown section
        mode_label = QLabel("Available Game Modes:")
        mode_label.setToolTip("Choose from available game modes")
        mode_layout.addWidget(mode_label)
        
        self.mode_dropdown = QComboBox()
        self.mode_dropdown.setToolTip("Select a game mode")
        self.mode_dropdown.addItems(["Standard", "Open", "Inverted"])  # Replace with actual modes
        self.mode_dropdown.currentTextChanged.connect(self.update_mode_info)
        mode_layout.addWidget(self.mode_dropdown)

        # Mode Info section
        mode_info_label = QLabel("Selected Mode Details:")
        mode_info_label.setToolTip("Description and details of the selected game mode")
        mode_layout.addWidget(mode_info_label)
        
        self.mode_info = QLabel("No mode selected")
        self.mode_info.setWordWrap(True)
        self.mode_info.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                min-height: 60px;
            }
        """)
        mode_layout.addWidget(self.mode_info)

        # Spoiler Checkbox
        self.spoiler_checkbox = QCheckBox("Enable Spoiler Log")
        self.spoiler_checkbox.setToolTip("Generate a spoiler log with this seed")
        mode_layout.addWidget(self.spoiler_checkbox)

        # Generate Button in a centered layout
        button_layout = QHBoxLayout()
        generate_button = QPushButton("Generate Seed")
        generate_button.setToolTip("Generate a new seed with the selected settings")
        generate_button.clicked.connect(self.generate_seed)
        generate_button.setFixedWidth(200)  # Set fixed width for the button
        button_layout.addStretch()
        button_layout.addWidget(generate_button)
        button_layout.addStretch()
        mode_layout.addLayout(button_layout)

        layout.addWidget(mode_group)
        layout.addStretch()

    def update_mode_info(self, selected_mode):
        """Update the mode info display when a game mode is selected"""
        if not selected_mode:
            self.mode_info.setText("No mode selected")
            return

        # This would be replaced with actual mode info parsing from yaml
        info_text = (
            f"Mode: {selected_mode}\n"
            f"Description: Sample description from yaml file\n"
            f"Settings: Example settings"
        )
        self.mode_info.setText(info_text)

    def is_spoiler_enabled(self):
        """Return whether spoiler log generation is enabled"""
        return self.spoiler_checkbox.isChecked()

    def generate_seed(self):
        """Generate a new seed with the selected settings"""
        selected_mode = self.mode_dropdown.currentText()
        spoiler_enabled = self.is_spoiler_enabled()
        print(f"Generating seed for mode: {selected_mode}, spoiler: {spoiler_enabled}")

    def refresh_preset_list(self):
        """Refresh the list of available presets"""
        print("Refreshing preset list")
