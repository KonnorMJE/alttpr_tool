import os
import pickle
import logging
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from alttpr_tool.config import Config

class GoogleServices:
    """Handles Google API authentication and service creation."""
    
    def __init__(self):
        """Initialize GoogleServices with necessary paths and scopes."""
        self.token_path = Config.TOKEN_PATH
        self.client_secrets_file = Config.CLIENT_SECRETS_FILE
        self.scopes = Config.GOOGLE_SCOPES
        self._credentials = None
        self._drive_service = None
        self._sheets_service = None

    def authenticate(self) -> Credentials:
        """
        Authenticate with Google API and return credentials.

        This method handles the authentication process with Google's API, using
        OAuth 2.0. If existing credentials are not found or are invalid, it prompts
        the user for re-authentication.

        Returns:
            Credentials: Authenticated Google API credentials.
            
        Raises:
            FileNotFoundError: If client secrets file is missing.
        """
        if self._credentials and self._credentials.valid:
            return self._credentials

        # Check for existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self._credentials = pickle.load(token)
                logging.info("Loaded existing credentials from token.pickle")

        # If no valid credentials available, prompt user to log in
        if not self._credentials or not self._credentials.valid:
            try:
                if (self._credentials and self._credentials.expired 
                    and self._credentials.refresh_token):
                    self._credentials.refresh(Request())
                    logging.info("Refreshed expired credentials")
            except RefreshError:
                os.remove(self.token_path)
                self._credentials = None
                logging.error("Token expired or revoked. Please re-authenticate.")

            if not self._credentials:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file,
                    self.scopes
                )
                self._credentials = flow.run_local_server(port=0)
                logging.info("Obtained new credentials")

            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(self._credentials, token)
                logging.info("Saved new credentials to token.pickle")

        return self._credentials

    def get_drive_service(self):
        """
        Create and return a Google Drive service object.

        Returns:
            Resource: Google Drive service object.
        """
        if not self._drive_service:
            creds = self.authenticate()
            self._drive_service = build('drive', 'v3', credentials=creds)
            logging.info("Google Drive service created")
        return self._drive_service

    def get_sheets_service(self):
        """
        Create and return a Google Sheets service object.

        Returns:
            Resource: Google Sheets service object.
        """
        if not self._sheets_service:
            creds = self.authenticate()
            self._sheets_service = build('sheets', 'v4', credentials=creds)
            logging.info("Google Sheets service created")
        return self._sheets_service

    def clear_credentials(self):
        """Clear stored credentials and services."""
        if os.path.exists(self.token_path):
            os.remove(self.token_path)
        self._credentials = None
        self._drive_service = None
        self._sheets_service = None
        logging.info("Cleared all credentials and services")