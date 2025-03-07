import asyncio
import logging
import os
import webbrowser
import yaml

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QPushButton, QFrame, QGroupBox,
                            QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt

from alttpr_tool.config import Config
from alttpr_tool.utilities.network import NetworkManager
from alttpr_tool.utilities.seed_generator import SeedGenerator


class GenerateSeedTab(QWidget):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.seed_generator = SeedGenerator()
        self.network_manager = NetworkManager()
        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

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
        self.mode_dropdown.currentTextChanged.connect(self.update_mode_info)
        self.mode_dropdown.setMaxVisibleItems(15)
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

        # Generate Button
        button_layout = QHBoxLayout()
        generate_button = QPushButton("Generate Seed")
        generate_button.setToolTip("Generate a new seed with the selected settings")
        generate_button.clicked.connect(self.generate_seed)
        generate_button.setFixedWidth(200)
        button_layout.addStretch()
        button_layout.addWidget(generate_button)
        button_layout.addStretch()
        mode_layout.addLayout(button_layout)

        layout.addWidget(mode_group)
        layout.addStretch()

    def refresh_data(self):
        """Refresh all data and update UI elements."""
        try:
            # Reset UI elements
            self.mode_dropdown.clear()
            self.mode_info.setText("No mode selected")
            self.spoiler_checkbox.setChecked(False)
            
            # Load fresh data
            self.preset_names = self.seed_generator.get_yaml_presets()
            if self.preset_names:
                self.mode_dropdown.addItems(self.preset_names)
                logging.info(f"Loaded {len(self.preset_names)} presets")
            else:
                logging.warning("No presets found")
                
        except Exception as e:
            logging.error(f"Error refreshing generate seed data: {e}")
            QMessageBox.warning(self, "Error", "Failed to load game modes")

    def update_mode_info(self, selected_mode):
        """
        Update the mode info display when a game mode is selected

        Args:
            selected_mode: The selected game mode
        """
        if not selected_mode:
            self.mode_info.setText("No mode selected")
            return
        else:
            try:
                preset_path = self.config.PRESETS_DIR / f"{selected_mode}.yaml"
                with open(preset_path, 'r') as f:
                    preset_data = yaml.safe_load(f)

                info_text = (
                    f"Mode: {selected_mode}\n"
                    f"Description: {preset_data.get('description', 'No description available')}\n"
                )
            except Exception as e:
                logging.error(f"Error loading preset {selected_mode}: {e}")
                info_text = f"Error loading preset {selected_mode}"

        self.mode_info.setText(info_text)

    def is_spoiler_enabled(self):
        """
        Return whether spoiler log generation is enabled

        Returns:
            bool: True if spoiler log generation is enabled, False otherwise
        """
        return self.spoiler_checkbox.isChecked()

    def generate_seed(self):
        """
        Generate a new seed with the selected settings

        Raises:
            Exception: If an error occurs during seed generation
        """
        if not self.network_manager.check_internet_connection():
            logging.error("No internet connection. Cannot generate seed.")
            messagebox.showerror("Error", "No internet connection. Cannot generate seed")
            return

        try:
            selected_mode = self.mode_dropdown.currentText()
            spoiler_enabled = self.is_spoiler_enabled()

            # Update the preset file with spoiler setting before generating
            self.update_preset_spoilers(selected_mode, spoiler_enabled)

            loop = asyncio.get_event_loop()
            seed = loop.run_until_complete(self.seed_generator.main_generate(selected_mode))

            if seed and hasattr(seed, 'url'):
                webbrowser.open(seed.url)
                logging.info(f"Seed URL opened in browser: {seed.url}")
            else:
                logging.warning("Generated seed does not have a URL or is None.")
        except Exception as e:
            logging.error(f"Error generating seed: {e}", exc_info=True)

    def refresh_preset_list(self):
        """
        Refresh the list of available presets

        Raises:
            Exception: If an error occurs during preset list refresh
        """
        print("Refreshing preset list")

    def update_preset_spoilers(self, preset_name, spoiler_enabled):
        """
        Update the spoiler setting in the preset file

        Args:
            preset_name: The name of the preset to update
            spoiler_enabled: Whether spoiler log generation is enabled
        """
        try:
            preset_path = self.config.PRESETS_DIR / f"{preset_name}.yaml"
            
            # Read current preset
            with open(preset_path, 'r') as f:
                preset_data = yaml.safe_load(f)

            # Update spoiler setting
            if 'settings' in preset_data:
                # Handle nested settings structure
                if isinstance(preset_data['settings'].get('spoilers', False), bool):
                    preset_data['settings']['spoilers'] = spoiler_enabled
                else:
                    preset_data['settings']['spoilers'] = "on" if spoiler_enabled else "off"
            else:
                # Handle root level settings
                if isinstance(preset_data.get('spoilers', False), bool):
                    preset_data['spoilers'] = spoiler_enabled
                else:
                    preset_data['spoilers'] = "on" if spoiler_enabled else "off"
            
            # Write updated preset back to file
            with open(preset_path, 'w') as f:
                yaml.safe_dump(preset_data, f, default_flow_style=False)

            logging.info(f"Updated spoiler setting to {spoiler_enabled} in preset {preset_name}")
            
        except Exception as e:
            logging.error(f"Error updating preset spoiler setting: {e}")
            raise
