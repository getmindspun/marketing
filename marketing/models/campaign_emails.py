""" Campaign email definitions """
import logging

import sqlalchemy
from sqlalchemy.orm import relationship

from .base import BASE
from .mixins import DefaultMixin


logger = logging.getLogger(__name__)


class EmailSendMethod(sqlalchemy.Enum):  # pylint: disable=too-many-ancestors
    """ Allowable ways to send the email """
    GMAIL = 1


class CampaignEmail(BASE, DefaultMixin):
    """
    The campaign_emails table
    """
    __tablename__ = "campaign_emails"

    campaign_id = sqlalchemy.Column(
        sqlalchemy.String(24),
        sqlalchemy.ForeignKey("campaigns.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        unique=False
    )

    template = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        unique=False
    )

    send_order = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
        default=0
    )

    send_delay = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
        default=0
    )

    send_method = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
        default=EmailSendMethod.GMAIL
    )

    campaign = relationship("Campaign", back_populates="emails")
