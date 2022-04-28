""" Google API Clients """
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from .settings import GOOGLE_API_SCOPES
from .gmail import Gmail


class GoogleApiClient:
    """ Client for Google APIs """

    def __init__(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(
                "token.json", GOOGLE_API_SCOPES
            )
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", GOOGLE_API_SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w", encoding="utf-8") as token:
                token.write(creds.to_json())
        self._credentials = creds

        self._gmail = None

    @property
    def gmail(self):
        """ Gmail service """
        if not self._gmail:
            self._gmail = Gmail(self._credentials)
        return self._gmail
