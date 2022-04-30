""" Pending emails """
import json
import logging

import sqlalchemy
from sqlalchemy.orm import relationship

from .base import BASE, Session
from .mixins import DefaultMixin

from .campaign_emails import CampaignEmail
from .campaigns import Campaign

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

    def as_data(self):
        """ Convert this object to template data """
        base = self.as_dict()
        data = base.pop("data")
        obj = json.loads(data) if data else {}
        obj.update(base)
        return obj

    @classmethod
    def delete_contact_from_campaign(
            cls,
            session: Session,
            contact_id: str,
            campaign_id: str,
            commit=True
    ) -> int:
        """ Remove all pending emails for this contact/campaign """
        count = session.query(Pending) \
            .filter(Pending.contact_id == contact_id,
                    Pending.campaign_email_id == CampaignEmail.id,
                    CampaignEmail.campaign_id == Campaign.id,
                    Campaign.id == campaign_id) \
            .delete(synchronize_session=False)
        if commit:
            session.commit()
        return count

    @classmethod
    def delete_for_contact(
            cls,
            session: Session,
            contact_id: str,
            commit=True
    ) -> int:
        """ Remove all pending emails for this contact/campaign """
        count = session.query(Pending) \
            .filter(Pending.contact_id == contact_id)\
            .delete(synchronize_session=False)
        if commit:
            session.commit()
        return count
