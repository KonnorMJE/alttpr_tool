import google.auth
import time
import logging

from googleapiclient.discovery import build

from alttpr_tool.config import Config
from alttpr_tool.utilities.google_services import GoogleServices

class GoogleSheetsData:
    """
    Class to interact with Google Sheets data, specifically for fetching and caching MSU data.
    """
    _data_cache = None
    _last_fetched_time = None

    try:
        service = GoogleServices().get_sheets_service()
        sheet = service.spreadsheets()
        logging.info("Google Sheets service established")
    except Exception as e:
        logging.error(f"Error when establishing connection to Google Sheets: {e}")

    @classmethod
    def convert_to_dict(cls, list_of_vals):
        """
        Converts a list of data into a list of dictionaries.

        Args:
            list_of_vals: List of values to be converted.

        Returns:
            List of dictionaries.
        """
        values = list_of_vals

        if not values:
            return []

        header = values[0]
        data_as_dict = [dict(zip(header, row)) for row in values[1:]]

        return data_as_dict

    @classmethod
    def _fetch_data_from_sheet(cls):
        """
        Fetches all data from the Google Sheet and updates the cache.

        Returns:
            Data fetched from the sheet as a list of dictionaries.
        """
        try:
            result = cls.sheet.values().get(spreadsheetId=Config().MSU_SHEET_ID, range="A:J").execute()
            values = result.get('values', [])
            cls._data_cache = cls.convert_to_dict(values)
            cls._last_fetched_time = time.time()
            logging.info("Data fetched from Google Sheet")
            return cls._data_cache
        except Exception as e:
            logging.error(f"Error fetching data from Google Sheet: {e}")
            return []

    @classmethod
    def get_all_data(cls):
        """
        Determines whether to use cached data or fetch fresh data from Google Sheet.

        Returns:
            List of MSU data.
        """
        current_time = time.time()

        if cls._data_cache is None or (current_time - cls._last_fetched_time) > FETCH_TIMEOUT_IN_SECONDS:
            cls._fetch_data_from_sheet()

        return cls._data_cache or []

    @classmethod
    def get_msu_names(cls):
        """
        Fetches a list of all MSU names from the cached Google Sheet data.

        Returns:
            List of MSU names.
        """
        if cls._data_cache:
            # return [entry['Pack Name'] for entry in cls._data_cache if entry['Download'].startswith("https://drive")]
            return [entry['Pack Name'] for entry in cls._data_cache if entry['Download'].startswith("https://") or entry['Download'].startswith("http://")]
        return []

    @classmethod
    def get_download_link(cls, msu_name):
        """
        Given an MSU name, fetches the corresponding download link from the cached data.

        Args:
            msu_name: Name of the MSU pack.

        Returns:
            Download link for the specified MSU pack.
        """
        if cls._data_cache:
            for entry in cls._data_cache:
                if entry['Pack Name'] == msu_name:
                    return entry['Download']

    @classmethod
    def get_msu_data(cls, msu_names):
        """
        Returns a list of dictionaries containing details for the specified MSU names.

        Args:
            msu_names: List of MSU names.

        Returns:
            List of dictionaries with MSU data.
        """
        if not cls._data_cache:
            return []
        
        result = []
        for msu_name in msu_names:
            for entry in cls._data_cache:
                if entry['Pack Name'] == msu_name:
                    result.append({
                        'Pack Name': entry['Pack Name'],
                        'Format': entry['Format'],
                        'Download': entry['Download']
                    })
                    break
        return result
