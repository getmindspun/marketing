""" Google API Clients """
from google.oauth2.service_account import Credentials

from marketing import settings
from .gmail import Gmail


class GoogleApiClient:
    """ Client for Google APIs """

    def __init__(self):
        credentials = Credentials.from_service_account_file(
            settings.GOOGLE_APPLICATION_CREDENTIALS,
            scopes=settings.GOOGLE_API_SCOPES
        )
        delegated_credentials = credentials.with_subject(settings.GOOGLE_USER)
        self._credentials = delegated_credentials
        self._gmail = None

    @property
    def gmail(self):
        """ Gmail service """
        if not self._gmail:
            self._gmail = Gmail(self._credentials)
        return self._gmail
