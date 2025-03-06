from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QPushButton, QFrame, QGroupBox)
from PyQt6.QtCore import Qt

class MSUSelectTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # SFC Selection Group
        sfc_group = QGroupBox("ROM Selection")
        sfc_group.setToolTip("Select the randomized ROM file to use")
        sfc_layout = QVBoxLayout(sfc_group)
        sfc_layout.setSpacing(10)

        # SFC Dropdown section
        sfc_label = QLabel("Available ROM Files:")
        sfc_label.setToolTip("Choose from available randomized ROMs")
        sfc_layout.addWidget(sfc_label)
        
        sfc_dropdown_layout = QHBoxLayout()
        self.sfc_dropdown = QComboBox()
        self.sfc_dropdown.setToolTip("Select a ROM file")
        self.sfc_dropdown.addItems(["ROM 1.sfc", "ROM 2.sfc", "ROM 3.sfc"])
        self.sfc_dropdown.currentTextChanged.connect(self.update_rom_info)
        
        sfc_refresh_button = QPushButton("Refresh")
        sfc_refresh_button.setToolTip("Refresh the list of available ROMs")
        sfc_refresh_button.clicked.connect(self.refresh_sfc_list)
        
        sfc_dropdown_layout.addWidget(self.sfc_dropdown)
        sfc_dropdown_layout.addWidget(sfc_refresh_button)
        sfc_layout.addLayout(sfc_dropdown_layout)

        # ROM Info section
        rom_info_label = QLabel("Selected ROM Details:")
        rom_info_label.setToolTip("Information about the selected ROM file")
        sfc_layout.addWidget(rom_info_label)
        
        self.rom_info = QLabel("No ROM selected")
        self.rom_info.setWordWrap(True)
        self.rom_info.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                min-height: 60px;
            }
        """)
        sfc_layout.addWidget(self.rom_info)

        layout.addWidget(sfc_group)

        # MSU Selection Group
        msu_group = QGroupBox("MSU Selection")
        msu_group.setToolTip("Select an MSU pack to use with your game")
        msu_layout = QVBoxLayout(msu_group)
        msu_layout.setSpacing(10)

        # MSU Dropdown section
        msu_label = QLabel("Available MSU Packs:")
        msu_label.setToolTip("Choose from your available MSU packs")
        msu_layout.addWidget(msu_label)
        
        msu_dropdown_layout = QHBoxLayout()
        self.msu_dropdown = QComboBox()
        self.msu_dropdown.setToolTip("Select an MSU pack")
        self.msu_dropdown.addItems(["MSU Pack 1", "MSU Pack 2", "MSU Pack 3"])
        
        msu_refresh_button = QPushButton("Refresh")
        msu_refresh_button.setToolTip("Refresh the list of available MSU packs")
        msu_refresh_button.clicked.connect(self.refresh_msu_list)
        
        msu_dropdown_layout.addWidget(self.msu_dropdown)
        msu_dropdown_layout.addWidget(msu_refresh_button)
        msu_layout.addLayout(msu_dropdown_layout)

        layout.addWidget(msu_group)

        # Actions Group
        actions_group = QGroupBox("Actions")
        actions_group.setToolTip("Available actions")
        actions_layout = QHBoxLayout(actions_group)
        
        back_button = QPushButton("Back")
        back_button.setToolTip("Return to the previous screen")
        back_button.clicked.connect(self.go_back)
        
        launch_button = QPushButton("Launch Game")
        launch_button.setToolTip("Launch the game with selected ROM and MSU pack")
        launch_button.clicked.connect(self.launch_game)
        
        actions_layout.addWidget(back_button)
        actions_layout.addStretch()
        actions_layout.addWidget(launch_button)

        layout.addWidget(actions_group)
        layout.addStretch()

    def update_rom_info(self, selected_rom):
        """Update the ROM info display when a ROM is selected"""
        if not selected_rom:
            self.rom_info.setText("No ROM selected")
            return

        # This would be replaced with actual ROM info parsing
        info_text = (
            f"ROM: {selected_rom}\n"
            f"Type: Randomized ALttP ROM\n"
            f"Size: 2MB"
        )
        self.rom_info.setText(info_text)

    def launch_game(self):
        print("Launch game clicked")

    def go_back(self):
        print("Back button clicked")

    def refresh_sfc_list(self):
        print("Refreshing ROM list")

    def refresh_msu_list(self):
        print("Refreshing MSU list") 