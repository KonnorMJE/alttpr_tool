import os
import logging

from config import BASE_DIR
from database.models import Configuration
from database.session import managed_session 

def get_user_settings():
    """
    Retrieve user settings from the database.

    :return: A dictionary of user settings.
    """
    with managed_session() as session:
        settings = session.query(Configuration).first()
        if settings:
            logging.info("User settings retrieved from database")
            return {
                "download_dir": settings.download_dir,
                "msu_master_dir": settings.msu_master_dir,
                "dark_mode": settings.dark_mode,
                "auto_run": settings.auto_run,
                "sfc_file": settings.sfc_file
            }
        else:
            logging.warning("No user settings found in database, returning default values")
            default_path = os.path.join(BASE_DIR, "CHANGEME")
            return {
                "download_dir": default_path,
                "msu_master_dir": default_path,
                "dark_mode": 0,
                "auto_run": 0,
                "sfc_file": None
            }

def save_settings_to_db(download_path, msu_master_path, dark_mode_var, auto_run_var):
    """
    Save user settings to the database.

    :param download_path: Path to the download directory.
    :param msu_master_path: Path to the MSU master directory.
    :param dark_mode_var: Dark mode setting.
    :param auto_run_var: Auto-run setting.
    """
    with managed_session() as session:
        settings = session.query(Configuration).first()

        if not settings:
            settings = Configuration(download_dir=download_path, msu_master_dir=msu_master_path, dark_mode=dark_mode_var, auto_run=auto_run_var)
            session.add(settings)
            logging.info("New user settings saved to database")
        else:
            settings.download_dir = download_path
            settings.msu_master_dir = msu_master_path
            settings.dark_mode = dark_mode_var
            settings.auto_run = auto_run_var
            logging.info("User settings updated in database")

def save_sfc_selection_to_db(selected_sfc):
    """
    Save the selected SFC file setting to the database.

    :param selected_sfc: The selected SFC file.
    """
    with managed_session() as session:
        settings = session.query(Configuration).first()

        if selected_sfc:
            full_sfc_path = os.path.join(settings.download_dir, selected_sfc)
            settings.sfc_file = full_sfc_path
            logging.info(f"SFC file selection saved to database: {full_sfc_path}")
        else:
            settings.sfc_file = ""
            logging.info("SFC file selection cleared in database")

def get_selected_sfc():
    """
    Retrieve the selected SFC file setting from the user settings.

    :return: Path to the selected SFC file.
    """
    user_settings = get_user_settings()
    if user_settings:
        logging.info(f"Retrieved selected SFC file from user settings: {user_settings.get('sfc_file')}")
        return user_settings.get("sfc_file")
    else:
        logging.warning("No selected SFC file found in user settings")
