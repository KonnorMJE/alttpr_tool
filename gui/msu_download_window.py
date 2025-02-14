import logging
import os
import re
import webbrowser

import customtkinter as ctk  # Keep this for background handling
import ttkbootstrap as ttk
from PIL import Image
import tkinter as tk
from tkinter import messagebox

from config import APP_HEIGHT, APP_WIDTH, DARK_DIR, LIGHT_DIR
import database.operations as db_ops
from utilities.download_queue import DownloadQueue
from utilities.google_drive import GoogleDriveData
from utilities.google_sheets import GoogleSheetsData

class MSUDownloadWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        logging.info("MSUDownloadWindow initialized")

        self.msus_from_google_sheets = []

        if self.controller.is_connected():

            self.sheets_data = GoogleSheetsData()
            
            logging.info("GoogleSheetsData initialized")

            if self.sheets_data.get_msu_names() == []:
                logging.debug("GoogleSheetsData.get_msu_names return an empty list. Fetching data...")
                self.sheets_data.get_all_data()

            self.msus_from_google_sheets = self.sheets_data.get_msu_names()

            logging.debug("MSU names fetched from Google Sheet")

        self.download_queue = DownloadQueue(all_downloads_complete_callback=self.show_download_report)

        self.download_outcomes = {"success": [], "fail": [], "manual": []}

        # Padding for the internal widgets

        self.background_image_file = 'Download.png'  # Define background image file name

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
        self.nav_menu.config(width=20)
        self.nav_menu.grid(row=0, column=0, sticky="nw")

        # Dropdown
        self.msu_dropdown = ttk.Combobox(self, values=self.msus_from_google_sheets)
        self.msu_dropdown.configure(state='readonly')
        self.msu_dropdown.grid(row=1, column=1, padx=15, pady=30, sticky="we")

        # Add Button
        self.add_button = ttk.Button(self, text="Add", command=self.add_msu, width=10)
        self.add_button.grid(row=1, column=0, padx=15, pady=30, sticky="n")

        # Remove Button
        self.remove_button = ttk.Button(self, text="Remove", command=self.remove_msu, width=10)
        self.remove_button.grid(row=2, column=0, padx=15, pady=15, sticky="n")

        # Download Button
        self.download_button = ttk.Button(self, text="Download", command=self.download_msus, width=10)
        self.download_button.grid(row=2, column=0, padx=15, pady=15, sticky="s")

        # Listboxes
        self.msus_to_download = tk.Listbox(self, width=45, height=10)
        self.msus_to_download.grid(row=2, column=1, padx=15, pady=15, sticky="wesn")

        # Back Button to go to Main Menu
        self.back_button = ttk.Button(self, text="Back", command=self.controller.show_main_window, width=10)
        self.back_button.grid(row=3, column=0, padx=15, pady=30)

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=375)
        self.progress_bar.grid(row=3, column=1, columnspan=2, padx=15, pady=30)
        self.progress_bar.set(0)

        for i in range(2):  # Iterates through a range to configure column weights
            self.grid_columnconfigure(i, weight=1)

    def update_progress_bar(self, value):
        """
        Updates the progress bar
        :param value: Value to update progress bar to
        """
        self.after(0, lambda: self.progress_bar.set(value / 100.0))
        logging.debug("Progress bar updated")

    def add_msu(self):
        """Adds the selected MSU from the dropdown to the msus_to_download listbox"""
        selection = self.msu_dropdown.get() # Gets the current dropdown/combobox selection

        # Adds the selection to the listbox if it's (the selection) not empty
        if selection:
            self.msus_to_download.insert(tk.END, selection)
            logging.info(f"Added MSU to download list: {selection}")
            file_id = self.extract_file_ids_from_links(self.sheets_data.get_download_link(selection))
            if not file_id:
                self.msus_to_download.itemconfig(tk.END, {'bg': 'orange'})
                self.download_outcomes["manual"].append(selection)
        else:
            logging.warning("Attempted to add an empty selection to the download list")


    def remove_msu(self):
        """Removes the selected MSU from the msus_to_download listbox"""
        selected = self.msus_to_download.curselection()
        if selected:
            msu_name = self.msus_to_download.get(selected)
            self.msus_to_download.delete(selected)
            
            # Remove the MSU from download outcomes if it exists
            for outcome in self.download_outcomes.values():
                if msu_name in outcome:
                    outcome.remove(msu_name)
            logging.info(f"Removed MSU from download list: {msu_name}")
        else:
            logging.warning("No MSU selected for removal")

    def get_list_to_download(self):
        """Iterates through the list of MSUs in the listbox and converts them to a list of download URLs"""
        self.selected_msus = list(self.msus_to_download.get(0, tk.END))
        msu_download_links = []
        for msu in self.selected_msus:
            msu_download_links.append(self.sheets_data.get_download_link(msu))
        return msu_download_links

    def extract_file_ids_from_links(self, link):
        """
        Extracts the file ID from a Google Drive sharing link.
        :param link: Google Drive sharing link.
        :return: File ID or None if the link is invalid.
        """

        # Regex patterns to match both types of URLs
        file_patterns = [
            r'^https?://drive\.google\.com/file/d/([^/]+)(/view\?.+)?',
            r'^https?://drive\.google\.com/open\?id=([^/]+)$'
        ]

        for pattern in file_patterns:
            match = re.match(pattern, link)
            if match:
                return match.group(1)

        return None

    def get_selected_msu_names(self):
        """
        Returns a list of all MSU names that the user has added to the listbox
        """
        return list(self.msus_to_download.get(0, tk.END))

    def make_completion_callback(self, index):
        def update_listbox_item(success, error=None):
            color = 'green' if success else 'red'
            self.msus_to_download.itemconfig(index, {'bg': color})
            msu_name = self.msus_to_download.get(index)
            if success:
                self.download_outcomes["success"].append(msu_name)
            else:
                failure_reason = f'{msu_name}: {error}' if error else msu_name
                self.download_outcomes["fail"].append(failure_reason)
        return update_listbox_item
    
    def show_download_report(self):
        report = "Download Report\n\n"
        report += "Successful Downloads:\n" + "\n".join(self.download_outcomes["success"]) + "\n\n"
        report += "Failed Downloads:\n" + "\n".join(self.download_outcomes["fail"]) + "\n\n"
        report += "Manual Downloads:\n" + "\n".join(self.download_outcomes["manual"])

        if messagebox.showinfo("Download Report", report) == "ok":
            self.open_manual_download_links()


    def open_manual_download_links(self):
        for msu_name in self.download_outcomes["manual"]:
            link = self.sheets_data.get_download_link(msu_name)
            webbrowser.open(link)

    def download_msus(self):
        def sanitize_file_names(file_name):
            return re.sub(r'[<>:"/\\|?*]', '-', file_name)
        
        # Reset progress bar to 0
        self.update_progress_bar(0)
        # Retrives a list of MSU Names from the listbox
        selected_msu_names = self.get_selected_msu_names()
        
        logging.info(f"Starting download for MSUs: {selected_msu_names}")

        # Fetch MSU data for the selected names.
        msu_data_list = self.sheets_data.get_msu_data(selected_msu_names)

        for i, msu_data in enumerate(msu_data_list):
            file_id = self.extract_file_ids_from_links(msu_data['Download'])
            if file_id:
                try:
                    # Extract the file ID from the download link
                    file_id = self.extract_file_ids_from_links(msu_data['Download'])
                    print(f'File ID from download_msus: {file_id}')
                    # Construct the file name using the pack name and format
                    if msu_data['Format'].lower() == "7-zip":
                        file_name = f"{msu_data['Pack Name']}.{'7z'}"
                    else:
                        file_name = f"{msu_data['Pack Name']}.{msu_data['Format'].lower()}"
                    # Sanitize file name
                    file_name = sanitize_file_names(file_name)
                    
                    # Determine the download destination path
                    dl_destination = os.path.join(db_ops.get_user_settings()['download_dir'], file_name)
                    
                    completion_callback = self.make_completion_callback(i)

                    self.download_queue.add_to_queue(file_id, dl_destination, GoogleDriveData.download_file, self.update_progress_bar, completion_callback)

                    logging.debug(f"Download {msu_data['Pack Name']} from {msu_data['Download']}")
                except Exception as e:
                    logging.error(f"Error downloading {msu_data['Pack Name']}: {e}", exc_info=True)
        if self.download_outcomes["manual"] and len(self.download_outcomes["manual"]) == len(selected_msu_names):
            self.show_download_report()

    def reset_window(self):
        logging.info("Resetting MSUDownloadWindow...")

        # Refresh the list of MSU names from Google Sheets.
        self.msus_from_google_sheets = self.sheets_data.get_msu_names()
        
        # Update the MSU dropdown with the latest data.
        self.msu_dropdown['values'] = self.msus_from_google_sheets

        # Clear the listbox containing MSUs queued for download.
        self.msus_to_download.delete(0, tk.END)
        self.download_outcomes = {"success": [], "fail": [], "manual": []}

        # Reset the progress bar to 0, indicating no current download progress.
        self.progress_bar.set(0)

        if db_ops.get_user_settings()['dark_mode'] == 0:
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')

        logging.info("MSUDownloadWindow reset complete.")