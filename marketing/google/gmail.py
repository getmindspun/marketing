""" GMAIL support """
import base64
import typing
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import addict

from googleapiclient.discovery import build

from marketing import utils, settings


class GmailDraft(addict.Dict):
    """ Gmail draft message """
    @property
    def subject(self) -> typing.Optional[str]:
        """ Draft subject """
        for header in self.message.payload.headers:
            if header.get("name", "").lower() == "subject":
                return header.get("value")
        return None

    # https://stackoverflow.com/a/24986452
    @staticmethod
    def _decode(text):
        text = text + "=" * (-len(text) % 4)
        text = text.replace("-", "+").replace("_", "/")
        return base64.b64decode(text).decode("utf8")

    def html(self):
        """ Return the HTML part of the draft """
        for part in self.message.payload.parts:
            if part.get("mimeType") == "text/html":
                return self._decode(part.body.data)
        return None

    def text(self):
        """ Return the text part of the draft """
        for part in self.message.payload.parts:
            if part.get(part.get("mimeType")) == "text/html":
                return self._decode(part.body.data)
        return None


class Gmail:
    """ Gmail service """
    def __init__(self, credentials):
        self.service = build(
            "gmail", "v1",
            credentials=credentials, cache_discovery=False
        )

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

    def get_draft_by_subject(
            self,
            subject: str
    ) -> typing.Optional[GmailDraft]:
        """ Find a draft be subject (the hard way) """
        for draft in self.drafts():
            if draft.subject == subject:
                return draft
        return None

    def send(
            self,
            message: MIMEBase,
            thread_id: str = None,
            user_id: str = "me"
    ) -> dict:
        """ Send an email """
        body = {
            "raw": base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        }
        if thread_id:
            body["threadId"] = thread_id

        return self.service.users().messages().send(
            userId=user_id, body=body
        ).execute()

    def send_draft(  # pylint: disable=too-many-arguments
            self,
            draft: GmailDraft,
            data: dict,
            email: str,
            sender: str = None,
            subject: str = None,
            message_id: str = None,
            thread_id: str = None,
            user_id: str = "me"
    ) -> dict:
        """ Send an email using the given draft """
        if not sender:
            sender = settings.SENDER

        if not subject:
            subject = utils.render(draft.subject, **data)

        msg = MIMEMultipart("alternative")
        msg["To"] = email
        msg["From"] = sender
        msg["Subject"] = subject

        if message_id:
            msg["In-Reply-To"] = message_id
            msg["References"] = message_id

        html = draft.html()
        if html:
            part = MIMEText(utils.render(html, **data), "html")
        else:
            part = MIMEText(utils.render(draft.text(), **data), "text")
        msg.attach(part)

        result = self.send(msg, thread_id=thread_id, user_id=user_id)
        result["subject"] = subject
        return result

    def get_message(self, message_id: str, user_id: str = "me") -> dict:
        """ Get a message by ID """
        result = self.service.users().messages().get(
            id=message_id, userId=user_id
        ).execute()
        return result

    def thread_responses(
            self,
            thread_id:
            str, user_id: str = "me",
            sender: str = None
    ) -> typing.List[dict]:
        """ Return a list of all response messages to the given thread """
        if sender is None:
            sender = settings.SENDER
        result = []
        messages = self.service.users().threads().get(
            userId=user_id, id=thread_id
        ).execute().get("messages")
        for msg in messages:
            if utils.get_message_header_value(msg, "From") != sender:
                result.append(msg)
        return result
