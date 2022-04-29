""" Contact model """
from datetime import datetime
import typing
import logging

import sqlalchemy
# from sqlalchemy.orm import relationship

from .base import BASE, Session
from .mixins import DefaultMixin


logger = logging.getLogger(__name__)


class Contact(BASE, DefaultMixin):
    """
    The contacts table
    """
    __tablename__ = "contacts"

    email = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        unique=True
    )

    unsubscribed_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        default=None,
        nullable=True,
    )

    @property
    def unsubscribed(self):
        """ Did this contact unsubscribe? """
        return self.unsubscribed_at is not None

    def unsubscribe(self):
        """ Mark this contact as unsubscribed """
        self.unsubscribed_at = datetime.utcnow()

    def resubscribe(self):
        """ Re-subscribe """
        self.unsubscribed_at = None

    @classmethod
    def get_by_email(
            cls,
            session: Session,
            email: str,
    ) -> typing.Optional["Contact"]:
        """ Find a contact by email address
        """
        return session.query(cls).filter(
            cls.email == email
        ).one_or_none()
