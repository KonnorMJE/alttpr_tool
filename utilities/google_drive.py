import io
import logging
import re

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from alttpr_tool.utilities.google_services import GoogleServices


class GoogleDriveData:
    try:
        service = GoogleServices().get_drive_service()
        logging.info("Google Drive service established")
    except Exception as e:
        logging.error(f"Error when establishing connection to Google Drive: {e}")

    @classmethod
    def download_file(cls, file_id, destination_path, callback=None):
        """
        Downloads a file from Google Drive.

        Args:
            file_id: ID of the file to be downloaded.
            destination_path: Local path to save the downloaded file.
            callback: Optional function to be called with the download progress.
        """
        try:
            request = cls.service.files().get_media(fileId=file_id)

            with io.FileIO(destination_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    progress = int(status.progress() * 100)
                    logging.info(f"Downloading chunk: {status.resumable_progress}/{status.total_size} - Progress: {progress}%")
                    if callback:
                        callback(int(status.progress() * 100))
            logging.info(f"File downloaded successfully to {destination_path}")
        except Exception as e:
            logging.error(f"Error downloading the file: {e}")
