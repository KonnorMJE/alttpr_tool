import logging
import os
from queue import Queue
import threading

from utilities.file_management import extract_msu, get_msu_dir


class DownloadQueue:
    def __init__(self, all_downloads_complete_callback=None):
        self.queue = Queue()
        self.is_downloading = False
        self.total_downloads = 0
        self.completed_downloads = 0
        self.all_downloads_complete_callback = all_downloads_complete_callback
        logging.info("Download queue initialized")

    def add_to_queue(self, file_id, destination_path, download_method, progress_callback=None, completion_callback=None):
        """
        Add a download task to the queue.

        :param file_id: File ID to be downloaded.
        :param destination_path: Path where the downloaded file will be saved.
        :param download_method: The method to use for downloading the file.
        :param progress_callback: Optional callback for download progress.
        :param completion_callback: Optional callback for download completion.
        """
        self.queue.put((file_id, destination_path, download_method, progress_callback, completion_callback))
        self.total_downloads += 1
        logging.info(f"Added file with ID {file_id} to download queue")
        self.start_next_download()

    def start_next_download(self):
        """
        Start the next download in the queue if the queue is not empty and no other download is in progress.
        """
        if not self.is_downloading and not self.queue.empty():
            self.is_downloading = True
            file_id, destination_path, download_method, progress_callback, completion_callback = self.queue.get()
            threading.Thread(target=self.download_file, args=(file_id, destination_path, download_method, progress_callback, completion_callback)).start()
            logging.info(f"Started download thread for file with ID {file_id}")

    def download_file(self, file_id, destination_path, download_method, progress_callback, completion_callback):
        """
        Download a file.

        :param file_id: File ID to be downloaded.
        :param destination_path: Path where the downloaded file will be saved.
        :param download_method: The method to use for downloading the file.
        :param progress_callback: Optional callback for download progress.
        :param completion_callback: Optional callback for download completion.
        """
        def on_progress(progress):
            if progress_callback:
                progress_callback(progress)

        try:
            download_method(file_id, destination_path, callback=on_progress)
            self.download_complete(destination_path, completion_callback, None)
        except Exception as e:
            logging.error(f'Error downloading file with ID {file_id}: {e}', exc_info=True)
            if completion_callback:
                completion_callback(False, str(e))
        finally:
            self.is_downloading = False
            self.start_next_download()

    def download_complete(self, destination_path, completion_callback, error=None):
        """
        Handle post-download actions and invoke completion callback.

        :param destination_path: Path where the downloaded file was saved.
        :param completion_callback: Callback for download completion.
        :param error: Optional error message if download failed.
        """
        self.completed_downloads += 1
        try:
            if error is None:
                msu_dir = get_msu_dir()
                extract_msu(destination_path, msu_dir)
                logging.info(f"Download complete, file extracted to {msu_dir}")

                if completion_callback:
                    completion_callback(True)
            else:
                logging.error(f"Error occurred during download: {error}")
                completion_callback(False, error)
        except Exception as e:
            logging.error(f'Error occurred during file extraction: {e}', exc_info=True)
            if completion_callback:
                completion_callback(False, e)
        finally:
            if self.completed_downloads == self.total_downloads:
                if self.all_downloads_complete_callback:
                    self.all_downloads_complete_callback()
                self.reset_download_tracking()

    def reset_download_tracking(self):
        """Resets the download tracking variables."""
        self.total_downloads = 0
        self.completed_downloads = 0
        self.is_downloading = False

    def is_queue_empty(self):
        """
        Check if the download queue is empty.
        :return: Current status of queue
        """
        return self.queue.empty()
