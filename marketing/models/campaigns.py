""" Campaign model """
import typing
import logging

import sqlalchemy
from sqlalchemy.orm import relationship

from .base import BASE, Session
from .mixins import DefaultMixin


logger = logging.getLogger(__name__)


class Campaign(BASE, DefaultMixin):
    """
    The campaigns table
    """
    __tablename__ = "campaigns"

    name = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        unique=True
    )

    @classmethod
    def get_by_name(
            cls,
            session: Session,
            name: str,
    ) -> typing.Optional["Campaign"]:
        """ Find a compaign by name
        """
        return session.query(cls).filter(
            cls.name == name
        ).one_or_none()

    emails = relationship(
        "CampaignEmail", back_populates="campaign",
        cascade="all, delete-orphan",
        order_by="CampaignEmail.send_order"
    )
