import logging
import os
import webbrowser
import yaml

import asyncio
import customtkinter as ctk  # Keep this for background handling
from tkinter import messagebox
import ttkbootstrap as ttk
from PIL import Image

from config import APP_HEIGHT, APP_WIDTH, BUTTON_WIDTH, DARK_DIR, LIGHT_DIR, PRESETS_DIR
from utilities.seed_generator import (get_yaml_presets,
                                      main_generate)
import database.operations as db_ops

class GenerateSeedWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        logging.info("GenerateSeedWindow initialized")

        self.button_width = 10

        self.preset_names = get_yaml_presets()  # Get list of presets from the presets dir

        logging.debug(f"Presets loaded: {self.preset_names}")

        self.background_image_file = 'Generate.png'  # Define the background image file name

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

        self.seed_preset_selection_label = ttk.Label(self, text="Please select the ALTTPR mode you'd like to generate a seed for")
        self.seed_preset_selection_label.grid(row=1, column=0, columnspan=2, padx=15, pady=15)

        self.seed_preset_selection_dropdown = ttk.Combobox(self, width=50, values=self.preset_names)
        self.seed_preset_selection_dropdown.configure(state='readonly')
        self.seed_preset_selection_dropdown.grid(row=2, column=0, columnspan=2, padx=15, pady=15)

        # Add spoiler checkbox
        self.spoiler_var = ttk.BooleanVar(value=False)
        self.spoiler_checkbox = ttk.Checkbutton(
            self, 
            text="Enable Spoiler Log",
            variable=self.spoiler_var
        )
        self.spoiler_checkbox.grid(row=3, column=0, padx=15, pady=15, columnspan=2)

        self.next_button = ttk.Button(self, text="Next", width=BUTTON_WIDTH, command=self.controller.show_sfc_selection_window)
        self.next_button.grid(row=4, column=0, padx=15, pady=15, sticky="e")
        
        self.generate_seed_button = ttk.Button(self, text="Generate", width=BUTTON_WIDTH, command=self.generate_seed)
        self.generate_seed_button.grid(row=4, column=1, padx=15, pady=15, sticky="w")

        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

    def generate_seed(self):
        if not self.controller.is_connected():
            logging.error("No internet connection. Cannot generate seed.")
            messagebox.showerror("Error", "No internet connection. Cannot generate seed")
            return

        try:
            preset_name = self.seed_preset_selection_dropdown.get()
            enable_spoilers = self.spoiler_var.get()

            # Update the preset file with spoiler setting before generating
            self.update_preset_spoilers(preset_name, enable_spoilers)

            loop = asyncio.get_event_loop()
            seed = loop.run_until_complete(main_generate(preset_name))

            if seed and hasattr(seed, 'url'):
                webbrowser.open(seed.url)
                logging.info(f"Seed URL opened in browser: {seed.url}")
            else:
                logging.warning("Generated seed does not have a URL or is None.")
                
        except Exception as e:
            logging.error(f"Error generating seed: {e}", exc_info=True)

    def update_preset_spoilers(self, preset_name, enable_spoilers):
        """Update the spoiler setting in the preset file."""
        try:
            preset_path = os.path.join(PRESETS_DIR, f"{preset_name}.yaml")
            
            # Read current preset
            with open(preset_path, 'r') as f:
                preset_data = yaml.safe_load(f)

            # Update spoiler setting
            if 'settings' in preset_data:
                # Handle nested settings structure
                if isinstance(preset_data['settings'].get('spoilers', False), bool):
                    preset_data['settings']['spoilers'] = enable_spoilers
                else:
                    preset_data['settings']['spoilers'] = "on" if enable_spoilers else "off"
            else:
                # Handle root level settings
                if isinstance(preset_data.get('spoilers', False), bool):
                    preset_data['spoilers'] = enable_spoilers
                else:
                    preset_data['spoilers'] = "on" if enable_spoilers else "off"

            # Write updated preset back to file
            with open(preset_path, 'w') as f:
                yaml.safe_dump(preset_data, f, default_flow_style=False)

            logging.info(f"Updated spoiler setting to {enable_spoilers} in preset {preset_name}")

        except Exception as e:
            logging.error(f"Error updating preset spoiler setting: {e}")
            raise

    def get_user_settings(self):
        return db_ops.get_user_settings()

    def reset_window(self):
        logging.info("Resetting GenerateSeedWindow...")

        self.seed_preset_selection_dropdown.set("")

        if self.get_user_settings()['dark_mode'] == 0:
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')

        logging.info("GenerateSeedWindow reset complete.")
