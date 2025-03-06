import logging
import os
import socket
import sys

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from config import APP_HEIGHT, APP_WIDTH, BASE_DIR, ICONS_DIR
from gui.generate_seed_window import GenerateSeedWindow
from gui.main_window import MainWindow
from gui.msu_download_window import MSUDownloadWindow
from gui.setup_window import SetupWindow
from gui.sfc_selection_window import SFCSelectionWindow
from utilities.file_management import get_download_dir, get_msu_dir
from utilities.initialize_db import initialize_db


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        initialize_db()
        logging.info("Database initialized")

        self.title("ALTTPR Tool")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.resizable(False, False)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.selected_frame = tk.StringVar()
        self.frame_names = {
            "Nav Menu": "Nav Menu",
            "Generate Seed": GenerateSeedWindow,
            "Select MSU": MainWindow,
            "Download MSUs": MSUDownloadWindow,
            "Settings": SetupWindow,
            "Select SFC": SFCSelectionWindow
        }

        self.frames = {}
        self.create_frames()

        if self.check_initial_setup():
            logging.info("Initial setup required, showing setup window")
            self.show_setup_window()
        else:
            logging.info("No initial setup required, showing generate seed window")
            self.show_generate_seed_window()

        logging.info("Application initialization completed")
        
        try:
            # First try the development path
            self.iconbitmap('gui/assets/icons/app-icon.ico')
        except:
            # If that fails, try the PyInstaller path
            import os
            import sys
            if getattr(sys, 'frozen', False):
                # If the application is run as a bundle
                application_path = sys._MEIPASS
            else:
                # If the application is run from a Python interpreter
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(application_path, 'gui', 'assets', 'icons', 'app-icon.ico')
            self.iconbitmap(icon_path)

    def on_select(self, selection):
        frame_class = self.frame_names[selection]
        self.show_frame(frame_class)

    def on_closing(self):
        """Handle application close event."""
        logging.info("Application is closing")
        self.destroy()
        sys.exit()

    def on_mousewheel(self, event, combobox):
        """Handle mousewheel event for combobox scrolling."""
        combobox.event_generate("<MouseWheel>", delta=event.delta)
        logging.debug(f"Mousewheel event generated for {combobox}")

    def get_base_dir(self):
        """Get the base directory of the application."""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return BASE_DIR
    
    def create_frames(self):
        """Create and initialize all frames (windows) for the application."""
        for F in (MainWindow, MSUDownloadWindow, SetupWindow, SFCSelectionWindow, GenerateSeedWindow):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            logging.debug(f"{F.__name__} frame created")

    def show_frame(self, context):
        """
        Show a specified frame.

        :param context: Frame class to be raised to the top.
        """
        frame = self.frames[context]
        if hasattr(frame, 'reset_window'):
            frame.reset_window()
            logging.debug(f"{context.__name__} frame reset")
        frame.tkraise()
        logging.info(f"{context.__name__} frame raised")
        self.selected_frame.set("Nav Menu")

    def show_setup_window(self):
        """Show the SetupWindow frame."""
        self.show_frame(SetupWindow)
        # self.selected_frame.set("Settings")

    def show_generate_seed_window(self):
        """Show the GenerateSeedWindow frame."""
        self.show_frame(GenerateSeedWindow)
        # self.selected_frame.set("Generate Seed")

    def show_sfc_selection_window(self):
        """Show the SFCSelectionWindow frame."""
        self.show_frame(SFCSelectionWindow)
        # self.selected_frame.set("Select SFC")
    
    def show_main_window(self):
        """Show the MainWindow frame."""
        self.show_frame(MainWindow)
        # self.selected_frame.set("Select MSU")

    def show_msu_download_window(self):
        """Show the MSUDownloadWindow frame if internet connection is available."""
        if not self.is_connected():
            logging.error("No internet connection. Cannot open MSUDownloadWindow")
            messagebox.showerror("Error", "No internet connection. Cannot open MSU Download Window.")
            return
        self.show_frame(MSUDownloadWindow)
        # self.selected_frame.set("Download MSUs")

    def is_default_or_nonexistent_path(self, path):
        """
        Check if a path is the default (CHANGEME) or does not exist.

        :param path: Path to check.
        :return: Boolean indicating if the path is default or non-existent.
        """
        is_default = os.path.basename(path) == "CHANGEME"
        is_nonexistent = not os.path.exists(path)
        if is_default or is_nonexistent:
            logging.debug(f"Path check for {path}: Default - {is_default}, Nonexistent - {is_nonexistent}")
        return is_default or is_nonexistent
    
    def check_initial_setup(self):
        """
        Check if initial setup is required based on download and MSU directories.

        :return: Boolean indicating if initial setup is needed.
        """
        download_dir = get_download_dir()
        msu_dir = get_msu_dir()
        need_setup = self.is_default_or_nonexistent_path(download_dir) or self.is_default_or_nonexistent_path(msu_dir)
        logging.info(f"Initial setup check: Needed - {need_setup}")
        return need_setup
    
    def is_connected(self, hostname="www.google.com"):
        """
        Check if there is an internet connection.

        :param hostname: Hostname to connect to for checking internet connectivity.
        :return: Boolean indicating if there is an internet connection.
        """
        try:
            host = socket.gethostbyname(hostname)
            s = socket.create_connection((host, 80), 2)
            s.close()
            logging.debug("Internet connection check: Connected")
            return True
        except Exception as e:
            logging.warning(f"Internet connection check failed: {e}")
        return False