import os
import logging
from pathlib import Path
from typing import Optional, Dict

from alttpr_tool.config import Config
from alttpr_tool.database.models import Configuration
from alttpr_tool.database.session import managed_session

class DatabaseOperations:
    """Handles all database operations for the application."""
    
    def __init__(self):
        """Initialize database operations."""
        self.config = Config()
        self.session = managed_session()
        
    def get_user_settings(self) -> Optional[Dict]:
        """
        Get user settings from database.
        
        Returns:
            Dict with settings or None if no settings exist
        """
        with managed_session() as session:
            settings = session.query(Configuration).first()
            if settings:
                return {
                    "download_dir": str(settings.download_dir),
                    "msu_master_dir": str(settings.msu_master_dir),
                    "tracker_path": str(settings.tracker_path) if settings.tracker_path else None,
                    "dark_mode": settings.dark_mode,
                    "auto_run": settings.auto_run,
                    "sfc_file": str(settings.sfc_file) if settings.sfc_file else None
                }
            return None

    def save_settings_to_db(self, download_dir: str, msu_master_dir: str, 
                           tracker_path: str, dark_mode: bool, auto_run: bool) -> None:
        """
        Save user settings to database.
        
        Args:
            download_dir: Path to download directory
            msu_master_dir: Path to MSU master directory
            tracker_path: Path to tracker application
            dark_mode: Dark mode enabled state
            auto_run: Auto run enabled state
        """
        with managed_session() as session:
            settings = session.query(Configuration).first()
            if not settings:
                settings = Configuration()
                session.add(settings)
            
            # Convert all paths to strings
            settings.download_dir = str(download_dir)
            settings.msu_master_dir = str(msu_master_dir)
            settings.tracker_path = str(tracker_path) if tracker_path else None
            settings.dark_mode = dark_mode
            settings.auto_run = auto_run

    def save_sfc_selection(self, selected_sfc: str) -> None:
        """
        Save the selected SFC file setting to the database.
        
        Args:
            selected_sfc: Path to selected SFC file
        """
        with managed_session() as session:
            settings = session.query(Configuration).first()
            
            if settings:
                if selected_sfc:
                    full_sfc_path = Path(settings.download_dir) / selected_sfc
                    settings.sfc_file = str(full_sfc_path)
                    logging.info(f"SFC file selection saved to database: {full_sfc_path}")
                else:
                    settings.sfc_file = ""
                    logging.info("SFC file selection cleared in database")

    def get_selected_sfc(self) -> str:
        """
        Retrieve the selected SFC file setting.
        
        Returns:
            str: Path to selected SFC file or None
        """
        settings = self.get_user_settings()
        if settings:
            sfc_file = settings.get("sfc_file")
            logging.info(f"Retrieved selected SFC file from settings: {sfc_file}")
            return sfc_file
        logging.warning("No selected SFC file found in settings")
        return None