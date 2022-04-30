""" Send pending emails """
import datetime
import logging
import time
import typing

import sqlalchemy

from . import settings, models, utils
from .google import GoogleApiClient

logger = logging.getLogger(__name__)


def emails_sent_in_last_day(session: models.Session) -> int:
    """ How many emails were sent in the last 24 hours """
    start_time = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    query = session.query(models.Sent.id).filter(
        models.Sent.sent_at >= start_time
    ).subquery()

    return session.execute(
        sqlalchemy.select(sqlalchemy.func.count()).select_from(query)
    ).scalar_one()


def pending(
        session: models.Session,
        limit: int = None
) -> typing.Iterable[models.Pending]:
    """ Iterator of pending emails """
    query = session.query(models.Pending)\
        .where(models.Pending.send_at < datetime.datetime.utcnow())\
        .order_by(models.Pending.send_at.asc())
    if limit:
        query = query.limit(limit)
    return query.all()


def send_one(
        client: GoogleApiClient,
        session: models.Session,
        email: models.Pending
) -> None:
    """ Send an email to one recipient """
    contact: models.Contact = email.contact
    campaign_email: models.CampaignEmail = email.campaign_email

    draft = client.gmail.get_draft_by_subject(campaign_email.template)
    if not draft:
        logger.error("Missing draft: %s", campaign_email.template)
        return

    data = email.as_data()
    data["email"] = contact.email

    session.delete(email)
    session.commit()

    # only if we successfully delete, send
    prior_email_id = data.pop("prior_email_id", None)
    if prior_email_id is None:
        # first email in the thread
        result = client.gmail.send_draft(draft, data, contact.email)
        logger.info("%s -> %s", contact.email, result["subject"])
        message = client.gmail.get_message(result["id"])
        message_id = utils.get_message_header_value(message, "Message-Id")
        thread_id = result["threadId"]
    else:
        prior_email = session.query(models.Sent).get(prior_email_id)
        if not prior_email:
            logger.warning("Prior email missing: %s", prior_email_id)
            return

        message_id = prior_email.message_id
        thread_id = prior_email.thread_id

        if client.gmail.thread_responses(thread_id=thread_id):
            logger.info("%s responded, ending drip", contact.email)
            models.Pending.delete(
                session,
                contact_id=contact.id,
                campaign_id=campaign_email.campaign_id
            )
            return

        subject = utils.render(prior_email.campaign_email.template, **data)
        result = client.gmail.send_draft(
            draft, data, contact.email, subject=subject,
            message_id=message_id, thread_id=thread_id
        )
        logger.info(
            "%s -> %s [followup]", contact.email, result["subject"]
        )

    sent = models.Sent.create(
        id=data["id"],
        contact_id=data["contact_id"],
        campaign_email_id=data["campaign_email_id"],
        sent_at=datetime.datetime.utcnow(),
        email_id=result["id"],
        message_id=message_id,
        thread_id=thread_id
    )
    session.add(sent)
    session.commit()


def send(session: models.Session = None, client: GoogleApiClient = None):
    """ Read pending and send """
    if session is None:
        session = models.Session()

    if client is None:
        client = GoogleApiClient()

    remaining = settings.MAX_EMAILS_PER_DAY - emails_sent_in_last_day(session)
    for email in pending(session, limit=remaining):  # exhaust cursor
        send_one(client, session, email)
        time.sleep(1)
