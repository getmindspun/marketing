""" Pending emails """
import logging

import sqlalchemy
from sqlalchemy.orm import relationship

from .base import BASE
from .mixins import DefaultMixin


logger = logging.getLogger(__name__)


class Pending(BASE, DefaultMixin):
    """
    The pending table
    """
    __tablename__ = "pending"

    contact_id = sqlalchemy.Column(
        sqlalchemy.String(24),
        sqlalchemy.ForeignKey("contacts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        unique=False
    )  # same as sent

    campaign_email_id = sqlalchemy.Column(
        sqlalchemy.String(24),
        sqlalchemy.ForeignKey("campaign_emails.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        unique=False
    )  # same as sent

    send_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
    )

    prior_email_id = sqlalchemy.Column(
        sqlalchemy.String(24),
        nullable=True
    )

    data = sqlalchemy.Column(
        sqlalchemy.Text,
        nullable=True
    )

    contact = relationship("Contact")
    campaign_email = relationship("CampaignEmail")
