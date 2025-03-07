import logging
import os
import platform
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import py7zr
import rarfile
import yaml

from alttpr_tool.config import Config
from alttpr_tool.database.operations import DatabaseOperations

class FileManager:
    """
    Handles file operations for MSUs and ROM files
    """
    
    def __init__(self):
        self.db = DatabaseOperations()
        self.user_settings = self.db.get_user_settings()
    
    def get_msu_dir(self) -> str:
        """
        Retrieve the MSU directory path from user settings.

        Returns:
            str: The MSU directory path.
        """
        try:
            msu_dir = self.user_settings.get("msu_master_dir")
            logging.info("MSU directory retrieved: %s", msu_dir)
            return msu_dir
        except Exception as e:
            logging.exception("Failed to retrieve MSU directory from user settings: %s", e)
            return None

    def get_download_dir(self) -> str:
        """
        Retrieve the download directory path from user settings.

        Returns:
            str: The download directory path.
        """
        try:
            if not self.user_settings:
                return None
            download_dir = self.user_settings.get('download_dir')
            if download_dir is None:
                raise ValueError("Download directory setting is missing")
            return download_dir
        except Exception as e:
            logging.error("An error occurred: %s", str(e))
            raise

    def get_sfc_files(self) -> list:
        """
        Get a list of .sfc files in the download directory.

        Returns:
            list: A list of .sfc files.
        """
        download_path = self.get_download_dir()
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

    def get_msus(self) -> list:
        """
        Get a list of MSU folders.

        Returns:
            list: A list of MSU folders.
        """
        msus_dir = self.get_msu_dir()
        try:
            os.makedirs(msus_dir, exist_ok=True)
            msu_entries = os.listdir(msus_dir)
            return [entry for entry in msu_entries 
                    if os.path.isdir(os.path.join(msus_dir, entry))]
        except Exception as e:
            logging.error(f"Error getting MSUs: {e}")
            return []

    def get_msu_name_convention(self, msu_name: str) -> str:
        """
        Get the naming convention of MSU files within a given MSU folder.

        Args:
            msu_name: The name of the MSU folder.

        Returns:
            str: The naming convention of MSU files within a given MSU folder.
        """
        msus_dir = self.get_msu_dir()
        try:
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

    def extract_msu(self, file_path: str, master_msu_dir: str):
        """
        Extract an MSU pack archive to the master MSU directory.

        Args:
            file_path: The path to the MSU pack archive.
            master_msu_dir: The path to the master MSU directory.
        """
        pack_name = self._extract_pack_name(file_path)
        extract_to = self._create_pack_directory(master_msu_dir, pack_name)
        
        try:
            self._extract_archive(file_path, extract_to)
            self._move_files_from_nested_dir(extract_to)
        finally:
            logging.info("Removing archive file: %s", file_path)
            os.remove(file_path)

    def _extract_pack_name(self, file_path: str) -> str:
        """
        Extract the pack name from the file path.

        Args:
            file_path: The path to the MSU pack archive.

        Returns:
            str: The pack name. 
        """
        return Path(file_path).stem

    def _create_pack_directory(self, master_msu_dir: str, pack_name: str) -> str:
        """
        Create a new directory for the pack.

        Args:
            master_msu_dir: The path to the master MSU directory.
            pack_name: The name of the pack.
        """
        pack_dir = Path(master_msu_dir) / pack_name
        pack_dir.mkdir(parents=True, exist_ok=True)
        return str(pack_dir)

    def _extract_archive(self, file_path: str, extract_to: str):
        """
        Extract the archive based on its type.

        Args:
            file_path: The path to the archive.
            extract_to: The path to the directory to extract to.
        """
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif file_path.endswith('.7z'):
            with py7zr.SevenZipFile(file_path, mode='r') as z_ref:
                z_ref.extractall(extract_to)
        elif file_path.endswith('.rar'):
            with rarfile.RarFile(file_path, mode='r') as r_ref:
                r_ref.extractall(extract_to)
        else:
            raise ValueError(f"Unsupported archive format: {file_path}")

    def _move_files_from_nested_dir(self, extract_to: str):
        """
        Move files from nested directories to the root extract directory.

        Args:
            extract_to: The path to the directory to extract to.
        """
        extract_path = Path(extract_to)
        for root, dirs, files in os.walk(extract_to, topdown=False):
            root_path = Path(root)
            if root_path != extract_path:
                for file in files:
                    src = root_path / file
                    dst = extract_path / file
                    shutil.move(str(src), str(dst))
                    logging.info("Moved file from %s to %s", src, dst)
                if not any(root_path.iterdir()):
                    root_path.rmdir()
                    logging.info("Removed empty directory: %s", root_path)