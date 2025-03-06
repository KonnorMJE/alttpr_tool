import os
import pickle
import logging

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Import from config file
from config import TOKEN_PATH, CLIENT_SECRETS_FILE, GOOGLE_SCOPES

def authenticate_service():
    """
    Authenticate with Google API and return credentials.

    This function handles the authentication process with Google's API, using
    OAuth 2.0. If existing credentials are not found or are invalid, it prompts
    the user for re-authentication.

    :return: Authenticated Google API credentials.
    """
    creds = None

    # Check for existing token.pickle file
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
            logging.info("Loaded existing credentials from token.pickle")

    # If no valid credentials are available, user is prompted to log in
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                logging.info("Refreshed expired credentials")
        except RefreshError:
            os.remove(TOKEN_PATH)
            creds = None
            logging.error("The authentication token has expired or been revoked. Please re-authenticate.")

        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                GOOGLE_SCOPES
            )
            creds = flow.run_local_server(port=0)
            logging.info("Ran authentication flow and obtained new credentials")

        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
            logging.info("Saved new credentials to token.pickle")

    return creds

def get_drive_service():
    """
    Create and return a Google Drive service object.

    :return: Google Drive service object.
    """
    creds = authenticate_service()
    service = build('drive', 'v3', credentials=creds)
    logging.info("Google Drive service created")
    return service

def get_sheets_service():
    """
    Create and return a Google Sheets service object.

    :return: Google Sheets service object.
    """
    creds = authenticate_service()
    service = build('sheets', 'v4', credentials=creds)
    logging.info("Google Sheets service created")
    return service