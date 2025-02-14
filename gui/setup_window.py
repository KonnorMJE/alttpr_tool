import os
import shutil
import logging

import customtkinter as ctk
import ttkbootstrap as ttk
from tkinter import StringVar, IntVar, messagebox, filedialog
from PIL import Image, ImageTk

from config import APP_HEIGHT, APP_WIDTH, BUTTON_WIDTH, BASE_DIR, DARK_DIR, LIGHT_DIR
import database.operations as db_ops

class SetupWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        logging.info("Initializing SetupWindow")

        self.download_path = StringVar()
        self.msu_master_path = StringVar()

        settings = self.get_user_settings()
        if settings:
            self.download_path.set(settings["download_dir"])
            self.msu_master_path.set(settings["msu_master_dir"])

        self.background_image_file = 'Settings.png'  # Define background image file name

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

        if db_ops.get_user_settings()['dark_mode'] == 0:
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')

        # Nav Menu
        if not self.controller.check_initial_setup():
            self.nav_menu = ttk.OptionMenu(self, self.controller.selected_frame, *self.controller.frame_names.keys(), command=controller.on_select)
            self.nav_menu.grid(row=0, column=0, sticky="nw")

        # Download Path Label & Entry
        self.download_label = ttk.Label(self, text="Download Path:")
        self.download_label.grid(row=1, column=0, padx=10, pady=(10, 5))

        self.download_entry = ttk.Entry(self, textvariable=self.download_path)
        self.download_entry.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="ew")

        self.download_path_button = ttk.Button(self, text="📁", command=self.set_download_entry)
        self.download_path_button.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="e")

        # MSU Master Path Label & Entry
        self.msu_label = ttk.Label(self, text="MSU Master Folder:")
        self.msu_label.grid(row=2, column=0, padx=10, pady=5)

        self.msu_entry = ttk.Entry(self, textvariable=self.msu_master_path)
        self.msu_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.msu_path_button = ttk.Button(self, text="📁", command=self.set_msu_entry)
        self.msu_path_button.grid(row=2, column=1, padx=10, pady=5, sticky="e")

        # Checkboxes
        self.dark_mode_var = IntVar(value=0)
        self.dark_mode_chk = ttk.Checkbutton(self, text="Dark Mode", variable=self.dark_mode_var)
        self.dark_mode_chk.grid(row=3, column=0, padx=10, pady=5)

        self.auto_run_var = IntVar(value=0)
        self.auto_run_chk = ttk.Checkbutton(self, text="Auto Run", variable=self.auto_run_var)
        self.auto_run_chk.grid(row=3, column=1, padx=10, pady=5)

        # Save & Cancel Buttons
        self.save_button = ttk.Button(self, text="Save", width=BUTTON_WIDTH, command=self.save_and_switch)
        self.save_button.grid(row=4, column=0, padx=10, pady=(5, 10))

        self.cancel_button = ttk.Button(self, text="Cancel", width=BUTTON_WIDTH, command=self.cancel_button_press)
        self.cancel_button.grid(row=4, column=1, padx=10, pady=(5, 10))

        # Configure columns for resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Configure rows
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            return folder_path
        
    def set_download_entry(self):
        download_path = self.select_folder()
        self.download_entry.delete(0, ttk.END)
        self.download_entry.insert(0, download_path)

    def set_msu_entry(self):
        msu_path = self.select_folder()
        self.msu_entry.delete(0, ttk.END)
        self.msu_entry.insert(0, msu_path)

    def get_user_settings(self):
        """Retrieve user settings from the database."""
        return db_ops.get_user_settings()

    def save_and_switch(self):
        """Save settings to the database and switch to the SFC selection window."""
        logging.info("Attempting to save settings and switch window")
        download_path = self.download_path.get().strip("\"")
        msu_master_path = self.msu_master_path.get().strip("\"")
        dark_mode = self.dark_mode_var.get()
        auto_run = self.auto_run_var.get()

        if self.controller.is_default_or_nonexistent_path(download_path):
            messagebox.showerror("Error", "Please input a valid Download Directory")
            return
        elif self.controller.is_default_or_nonexistent_path(msu_master_path):
            messagebox.showerror("Error", "Please input a valid MSU Directory")
            return
        else:
            if os.path.exists(os.path.join(BASE_DIR, 'CHANGEME')):
                shutil.rmtree(os.path.join(BASE_DIR, 'CHANGEME'))
            self.save_to_db(download_path, msu_master_path, dark_mode, auto_run)
            self.controller.show_sfc_selection_window()

    def cancel_button_press(self):
        """Handle cancel button press and show the main window or error message."""
        logging.info("Cancel button pressed in SetupWindow")
        download_dir = self.get_user_settings()["download_dir"]
        msu_master_dir = self.get_user_settings()["msu_master_dir"]
        if self.controller.is_default_or_nonexistent_path(download_dir):
            messagebox.showerror("Error", "Please change from the default 'CHANGEME' directory")
            return
        elif self.controller.is_default_or_nonexistent_path(msu_master_dir):
            messagebox.showerror("Error", "Please change from the default 'CHANGEME' directory")
            return
        else:
            self.controller.show_main_window()

    def save_to_db(self, download_path, msu_master_path, dark_mode_var, auto_run_var):
        """Save the provided settings to the database."""
        logging.info(f"Saving settings to database: {download_path}, {msu_master_path}, {dark_mode_var}, {auto_run_var}")
        db_ops.save_settings_to_db(download_path, msu_master_path, dark_mode_var, auto_run_var)
    
    def reset_window(self):
        """Reset the window to reflect the current settings."""
        logging.info("Resetting SetupWindow")
        settings = self.get_user_settings()

        if not self.controller.check_initial_setup():
            self.nav_menu = ttk.OptionMenu(self, self.controller.selected_frame, *self.controller.frame_names.keys(), command=self.controller.on_select)
            self.nav_menu.grid(row=0, column=0, sticky="nw")

        if settings:
            self.download_path.set(settings["download_dir"])
            self.msu_master_path.set(settings["msu_master_dir"])
            self.dark_mode_var.set(settings["dark_mode"])
            self.auto_run_var.set(settings["auto_run"])
        else:
            self.download_path.set("")
            self.msu_master_path.set("")
            self.dark_mode_var.set(0)
            self.auto_run_var.set(0)

        if settings and settings.get('dark_mode') == 0:
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')
        logging.info("SetupWindow reset complete")