import os
import logging

import customtkinter as ctk  # Keep this for background handling
import ttkbootstrap as ttk
from PIL import Image

from config import APP_HEIGHT, APP_WIDTH, BUTTON_WIDTH, DARK_DIR, LIGHT_DIR
from database.operations import get_user_settings, save_sfc_selection_to_db
from utilities.file_management import get_sfc_files

class SFCSelectionWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        logging.info("Initializing SFCSelectionWindow")

        self.sfc_files = get_sfc_files()  # Get SFC files from downloads folder
        self.background_image_file = 'SFCFileSelect.png'  # Define background image file name

        # Create background frame to hold background image & place it.
        self.background_frame = ctk.CTkFrame(self)
        self.background_frame.place(x=0, y=0, relwidth=1, relheight=1) 

        # Create light and dark mode background images
        self.light_image = Image.open(os.path.join(LIGHT_DIR, self.background_image_file)) 
        self.dark_image = Image.open(os.path.join(DARK_DIR, self.background_image_file)) 

        # Create customtkinter image with the light and dark images
        self.bg_image = ctk.CTkImage(light_image=self.light_image, dark_image=self.dark_image, size=(APP_WIDTH, APP_HEIGHT))

        # Nav Menu
        self.nav_menu = ttk.OptionMenu(self, self.controller.selected_frame, *self.controller.frame_names.keys(), command=controller.on_select)
        self.nav_menu.grid(row=0, column=0, sticky="nw")
        
        # Create and place label for holding the background image
        self.bg_image_label = ctk.CTkLabel(self.background_frame, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # Label
        self.sfc_selection_label = ttk.Label(self, text="Please select the .sfc ALTTPR file you'd like to proceed with")
        self.sfc_selection_label.grid(row=1, column=0, columnspan=2, padx=15, pady=15)

        # Dropdown
        self.sfc_selection_dropdown = ttk.Combobox(self, width=60, values=self.sfc_files)
        self.sfc_selection_dropdown.configure(state='readonly')
        self.sfc_selection_dropdown.grid(row=2, column=0, columnspan=2, padx=15, pady=15)

        # Next Button (To Select MSU window)
        self.to_main_button = ttk.Button(self, text="Next", width=13, command=self.confirm_and_switch)
        self.to_main_button.grid(row=3, column=0, padx=15, pady=15, sticky="e")

        #
        self.to_generate_button = ttk.Button(self, text="Back", width=13, command=self.controller.show_generate_seed_window)
        self.to_generate_button.grid(row=3, column=1, padx=15, pady=15, sticky="w")

        for i in range(2):  # Iterates through a range to configure column weights
            self.grid_columnconfigure(i, weight=1)

    def reset_window(self):
        """Reset the window to update the list of .sfc files and user settings."""
        logging.info("Resetting SFCSelectionWindow")
        self.sfc_files = get_sfc_files()

        self.sfc_selection_dropdown['values'] = self.sfc_files
        self.sfc_selection_dropdown.set(self.sfc_files[0] if self.sfc_files else "")

        if self.get_user_settings()['dark_mode'] == 0:
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')
        logging.info("SFCSelectionWindow reset complete")

    def get_user_settings(self):
        """Retrieve user settings from the database."""
        return get_user_settings()

    def confirm_and_switch(self):
        """Confirm the selected .sfc file and switch to the main window."""
        logging.info("Confirming SFC selection and switching to MainWindow")
        selected_sfc = self.sfc_selection_dropdown.get()

        save_sfc_selection_to_db(selected_sfc)
        logging.debug(f"Selected SFC: {selected_sfc}")

        self.controller.show_main_window()
