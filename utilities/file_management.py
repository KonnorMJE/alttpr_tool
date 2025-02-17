import logging
import os
import platform
import shutil
import subprocess
import sys
import zipfile

import py7zr
import rarfile
import yaml

from config import BASE_DIR, PRESETS_DIR
from database.operations import get_user_settings

def get_msu_dir():
    """Retrieve the MSU directory path from user settings."""
    try:
        user_settings = get_user_settings()
        msu_dir = user_settings.get("msu_master_dir")
        logging.info("MSU directory retrieved: %s", msu_dir)
        return msu_dir
    except Exception as e:
        logging.exception("Failed to retrieve MSU directory from user settings: %s", e)
        return None

def get_download_dir():
    """Retrieve the download directory path from user settings."""
    try:
        user_settings = get_user_settings()
        if not user_settings:
            return None
        download_dir = user_settings.get('download_dir')
        if download_dir is None:
            raise ValueError("Download directory setting is missing")
        return download_dir
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        raise

def get_sfc_files():
    """Get a list of .sfc files in the download directory."""
    download_path = get_download_dir()
    try:
        download_files = os.listdir(download_path)
        sfc_files = [file for file in download_files if file.endswith('.sfc')]
        logging.info("SFC files retrieved: %s", sfc_files)
        return sfc_files
    except FileNotFoundError:
        logging.error("The directory %s does not exist.", download_path)
        raise
    except Exception as e:
        logging.exception("An unexpected error occurred: %s", e)
        raise

def get_msus():
    """Get list of MSU folders."""
    msus_dir = get_msu_dir()
    try:
        # Create directory if it doesn't exist
        os.makedirs(msus_dir, exist_ok=True)
        
        msu_entries = os.listdir(msus_dir)
        return [entry for entry in msu_entries 
                if os.path.isdir(os.path.join(msus_dir, entry))]
    except Exception as e:
        logging.error(f"Error getting MSUs: {e}")
        return []

def get_msu_name_convention(msu_name):
    """Get the naming convention of MSU files within a given MSU folder."""
    msus_dir = get_msu_dir()
    try:
        full_msu_path = os.path.join(msus_dir, msu_name)
        msu_file_found = False
        naming_convention = None

        for file in os.listdir(full_msu_path):
            if file.endswith(".msu"):
                msu_file_found = True
                naming_convention = os.path.splitext(file)[0]
                break
            elif file.endswith(".pcm") and not msu_file_found:
                if file.count("-") == 1:
                    naming_convention = file.split('-', 1)[0]

        if naming_convention:
            return naming_convention
        else:
            logging.exception(f"No valid MSU or PCM files found in {msu_name}")
            raise ValueError(f"No valid MSU or PCM files found in {msu_name}")

    except FileNotFoundError:
        logging.exception(f"The MSU folder {msu_name} does not exist in {msus_dir}")
        raise
    except Exception as e:
        logging.exception("An error occurred while getting MSU naming convention")
        raise


def rmv_existing_sfc(msu_name, naming_conv):
    msus_dir = get_msu_dir()
    try:
        full_msu_dir = get_full_msu_dir(msu_name)
        existing_sfc = f"{naming_conv}.sfc"
        full_path_to_msu = os.path.join(full_msu_dir, existing_sfc)

        if os.path.exists(full_path_to_msu):
            logging.info("Removing existing SFC file: %s", full_path_to_msu)
            os.remove(full_path_to_msu)
    except FileNotFoundError:
        logging.error("File or directory not found: %s", full_path_to_msu)
        raise
    except Exception as e:
        logging.exception("An error occurred while trying to delete the existing .sfc file: %s", e)
        raise
    
def move_file(current_path, new_path):
    shutil.move(current_path, new_path)

def get_full_msu_dir(msu_name):
    msus_dir = get_msu_dir()
    full_msu_dir = os.path.join(msus_dir, msu_name)
    return full_msu_dir

def extract_pack_name(file_path):
    """
    Extracts the pack name from the file path.

    :param file_path: The path to the archive file.
    :return: The pack name.
    """
    base_name = os.path.basename(file_path)
    pack_name, _ = os.path.splitext(base_name)
    return pack_name

def create_pack_directory(master_msu_dir, pack_name):
    """
    Creates a new directory for the pack within the master MSU directory.

    :param master_msu_dir: The master MSU directory.
    :param pack_name: The name of the pack.
    :return: The path to the new pack directory.
    """
    pack_dir = os.path.join(master_msu_dir, pack_name)
    if not os.path.exists(pack_dir):
        os.makedirs(pack_dir)
    return pack_dir

def extract_msu(file_path, master_msu_dir):
    """
    Extracts an MSU pack archive to a new directory within the master MSU directory.
    
    :param file_path: The path to the archive file.
    :param master_msu_dir: The master MSU directory.
    """
    pack_name = extract_pack_name(file_path)
    extract_to = create_pack_directory(master_msu_dir, pack_name)
    seven_zip_path = os.path.join(BASE_DIR, '7z/7z.exe')
    
    try:
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif file_path.endswith('.7z'):
            if platform.system() == 'Windows':
                subprocess.check_call([seven_zip_path, 'x', '-o' + extract_to, file_path])
            else:
                with py7zr.SevenZipFile(file_path, mode='r') as z_ref:
                    z_ref.extractall(extract_to)
        elif file_path.endswith('.rar'):
            if platform.system() == 'Windows':
                subprocess.check_call([seven_zip_path, 'x', '-o' + extract_to, file_path])
            else:
                with rarfile.RarFile(file_path, mode='r') as r_ref:
                    r_ref.extractall(extract_to)
        else:
            logging.error("Unsupported archive format: %s", file_path)
            raise ValueError("Unsupported archive format.")
    except subprocess.CalledProcessError as e:
        logging.error("7-Zip failed to extract file: %s", e)
        raise
    except Exception as e:
        logging.exception("Failed to extract MSU pack: %s", e)
        raise
    finally:
        logging.info("Removing archive file: %s", file_path)
        os.remove(file_path)
    
    # After extraction, check for nested directory and move files if necessary
    move_files_from_nested_dir(extract_to)

def move_files_from_nested_dir(extract_to):
    """
    Moves files from a nested directory to the intended directory if needed.
    """
    try:
        for root, dirs, files in os.walk(extract_to):
            for file in files:
                file_path = os.path.join(root, file)
                if root != extract_to: 
                    shutil.move(file_path, extract_to)
                    logging.info("Moved file from %s to %s", file_path, extract_to)

            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if dir_path != extract_to and root != extract_to:
                    new_dir_path = os.path.join(extract_to, dir)
                    shutil.move(dir_path, new_dir_path)
                    logging.info("Moved directory from %s to %s", dir_path, new_dir_path)

            if root != extract_to and not os.listdir(root):
                os.rmdir(root)
                logging.info("Removed empty directory: %s", root)
    except Exception as e:
        logging.exception("An error occurred while moving files from nested directories: %s", e)
        raise