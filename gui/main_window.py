import logging
import os
import platform
import subprocess

import customtkinter as ctk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from tkinter import messagebox

from config import APP_HEIGHT, APP_WIDTH, BUTTON_WIDTH, DARK_DIR, LIGHT_DIR
from database.operations import get_selected_sfc, get_user_settings
from utilities.file_management import get_full_msu_dir, get_msus, get_msu_name_convention, move_file, rmv_existing_sfc

class MainWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        logging.info("MainWindow initialized")

        self.msu_folders = get_msus()
        
        logging.debug(f"MSU folders loaded: {self.msu_folders}")

        # Define background image file name
        self.background_image_file = 'MSUSelect.png'

        # Create background frame to hold background image & place it.
        self.background_frame = ctk.CTkFrame(self)
        self.background_frame.place(x=0, y=0, relwidth=1, relheight=1) 

        # Create light and dark mode background images
        self.light_image = Image.open(os.path.join(LIGHT_DIR, self.background_image_file)) 
        self.dark_image = Image.open(os.path.join(DARK_DIR, self.background_image_file)) 

        # Create customtkinter image with the light and dark images
        self.bg_image = ctk.CTkImage(light_image=self.light_image, dark_image=self.dark_image, size=(APP_WIDTH, APP_HEIGHT))
        
        # Create and place label for holding the background image
        self.bg_image_label = ctk.CTkLabel(self.background_frame, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # Nav Menu
        self.nav_menu = ttk.OptionMenu(self, self.controller.selected_frame, *self.controller.frame_names.keys(), command=controller.on_select)
        self.nav_menu.grid(row=0, column=0, sticky="nw")

        # Label
        self.msu_select_label = ttk.Label(self, text="Select the MSU you'd like to use")
        self.msu_select_label.grid(row=1, column=0, padx=15, pady=15)

        # Dropdown
        self.msu_select_dropdown = ttk.Combobox(self, width=50, values=self.msu_folders)
        self.msu_select_dropdown.configure(state='readonly')
        self.msu_select_dropdown.grid(row=2, column=0, padx=15, pady=15)

        # Button to Confirm MSU Selection
        self.confirm_button = ttk.Button(self, text="Confirm", width=BUTTON_WIDTH, command=self.confirm_msu_selection)
        self.confirm_button.grid(row=3, column=0, padx=60, pady=15, sticky="w")

        # Button to Settings Window
        self.settings_button = ttk.Button(self, text="Settings", width=BUTTON_WIDTH, command=self.controller.show_setup_window)
        self.settings_button.grid(row=3, column=0, padx=60, pady=15)

        # Button to MSU Download Window
        self.msu_download_button = ttk.Button(self, text="Download MSUs", width=15, command=self.controller.show_msu_download_window)
        self.msu_download_button.grid(row=3, column=0, padx=60, pady=15, sticky="e")

        # Button to go back to SFC Selection Window
        self.back_button = ttk.Button(self, text="Back", width=10, command=self.controller.show_sfc_selection_window)
        self.back_button.grid(row=4, column=0, padx=15, pady=15)

        # Iterates through a range to configure column weights
        for i in range(1):
            self.grid_columnconfigure(i, weight=1)

    def reset_window(self):
        """Resets the GUI widgets state within the frame."""
        
        logging.info("Resetting MainWindow...")
        
        self.msu_folders = get_msus()
        
        logging.debug(f"MSU folders: {self.msu_folders}")

        # Update the dropdown with the refreshed list of MSU folders.
        self.msu_select_dropdown['values'] = self.msu_folders

        # Clear the current selection in the dropdown.
        self.msu_select_dropdown.set("")

        # Pre-select the first item in the dropdown if available.
        if self.msu_folders:
            self.msu_select_dropdown.set(self.msu_folders[0])

        # Force update the dropdown (may not be necessary, but can be tried if all else fails)
        self.msu_select_dropdown.update()

        # Destroy the old dropdown
        self.msu_select_dropdown.destroy()

        # Recreate the dropdown with the refreshed list of MSU folders.
        self.msu_select_dropdown = ttk.Combobox(self, width=50, values=self.msu_folders)
        self.msu_select_dropdown.configure(state='readonly')
        self.msu_select_dropdown.grid(row=2, column=0, padx=15, pady=15)

        # Set the default value if available
        if self.msu_folders:
            self.msu_select_dropdown.set(self.msu_folders[0])

        if self.get_user_settings()['dark_mode'] == 0:
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')

        logging.info("MainWindow reset complete.")

    def get_user_settings(self):
        return get_user_settings()

    def get_selected_msu(self):
        """
        Get selected MSU from the dropdown
        
        :return: Selected MSU from the dropdown, pulling from the set MSU Master Dir
        """

        return self.msu_select_dropdown.get()
    
    def run_sfc(self, path):
        try:
            if platform.system() == 'Windows':
                os.startfile(path)
            elif platform.system() == 'Darwin':
                subprocess.run(['open', path])
            else:
                subprocess.run(['xdg-open', path])
        except Exception as e:
            logging.error(f"Failed to open file: {e}", exc_info=True)
            raise

    def confirm_msu_selection(self):
        msu = self.get_selected_msu()
        logging.info(f"MSU selected: {msu}")
        naming_convention = get_msu_name_convention(msu)
        logging.debug(f'Naming Conv: {naming_convention}')
        new_file_name = f"{naming_convention}.sfc"
        logging.debug(f'New file name: {new_file_name}')
        rmv_existing_sfc(msu, naming_convention)
        sfc_file = get_selected_sfc()
        if sfc_file == "":
            messagebox.showerror("Error", "No SFC file downloaded.")
        else:
            logging.debug(f'SFC File: {sfc_file}')
            new_sfc_path = os.path.join(get_full_msu_dir(msu), new_file_name)  # Pass msu to get_full_msu_dir
            logging.debug(f'New SFC Path: {new_sfc_path}')
            move_file(sfc_file, new_sfc_path)

            if os.path.exists(new_sfc_path):
                messagebox.showinfo("Info", f"SFC successfully moved to {get_full_msu_dir(msu)}")
                if get_user_settings()['auto_run'] == 1:
                    self.run_sfc(new_sfc_path)
