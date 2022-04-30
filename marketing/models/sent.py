""" Pending emails """
from datetime import datetime
import logging

import sqlalchemy
from sqlalchemy.orm import relationship

from .base import BASE
from .mixins import DefaultMixin


logger = logging.getLogger(__name__)


class Sent(BASE, DefaultMixin):
    """
    The sent table
    """
    __tablename__ = "sent"

    contact_id = sqlalchemy.Column(
        sqlalchemy.String(24),
        sqlalchemy.ForeignKey("contacts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        unique=False
    )  # same as pending

    campaign_email_id = sqlalchemy.Column(
        sqlalchemy.String(24),
        sqlalchemy.ForeignKey("campaign_emails.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        unique=False
    )  # same as pending

    sent_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        index=True
    )

    opened_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
    )

    prior_email_id = sqlalchemy.Column(
        sqlalchemy.String(24),
        nullable=True
    )

    email_id = sqlalchemy.Column(
        sqlalchemy.String(64),
        nullable=False
    )

    message_id = sqlalchemy.Column(
        sqlalchemy.String(256),
        nullable=False
    )

    thread_id = sqlalchemy.Column(
        sqlalchemy.String(64),
        nullable=False
    )

    contact = relationship("Contact")
    campaign_email = relationship("CampaignEmail")

    def open(self) -> None:
        """ Mark this email as opened """
        self.opened_at = datetime.utcnow()

    def opened(self) -> bool:
        """ Was this email opened? s"""
        return self.opened_at is not None
