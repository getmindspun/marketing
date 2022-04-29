""" GMAIL support """
import base64
import typing
from email.mime.base import MIMEBase

import addict

from googleapiclient.discovery import build


class GmailDraft(addict.Dict):
    """ Gmail draft message """
    @property
    def subject(self) -> typing.Optional[str]:
        """ Draft subject """
        for header in self.message.payload.headers:
            if header.get("name", "").lower() == "subject":
                return header.get("value")
        return None


class Gmail:
    """ Gmail service """
    def __init__(self, credentials):
        self.service = build("gmail", "v1", credentials=credentials)

    def drafts(self, user_id="me") -> typing.Iterator[GmailDraft]:
        """ List all drafts """
        results = self.service.users().drafts().list(userId=user_id).execute()
        drafts = results.get("drafts", [])
        if drafts:
            for draft in drafts:
                yield GmailDraft(
                    self.service.users().drafts().get(
                        userId=user_id, id=draft["id"]
                    ).execute()
                )

    def send(self, message: MIMEBase, user_id="me"):
        """ Send an email """
        body = {
            "raw": base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        }
        return self.service.users().messages().send(
            userId=user_id, body=body
        ) .execute()
