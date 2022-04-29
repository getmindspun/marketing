""" Model mixins """
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.declarative import declared_attr

import bson.objectid

from marketing import utils


def oid() -> str:
    """ Generate a random object id """
    return str(bson.objectid.ObjectId())


class ObjectIdMixin:
    """ Mixin that add a 24 character id column """
    @staticmethod
    def generate_oid() -> str:
        """ Generator for the id """
        return oid()

    id = sqlalchemy.Column(
        sqlalchemy.String(24),
        primary_key=True,
        default=oid
    )


def model_as_dict(model) -> dict:
    """Convert given sqlalchemy model to dict (relationships not included)."""
    result = {}
    for attr in sqlalchemy.inspect(model).mapper.column_attrs:
        value = getattr(model, attr.key)
        if isinstance(value, datetime):
            value = utils.isoformat(value)
        # elif isinstance(value, uuid.UUID):
        #    value = str(value)
        result[attr.key] = value
    return result


class CreateMixin:
    """ Adds a create() class method """
    @classmethod
    def create(cls, *args, **kwargs):
        """ Create an instance (with generic args) """
        return cls(*args, **kwargs)  # noqa


class DictMixin:
    """ Mixin to add as_dict() """
    # pylint: disable=too-few-public-methods

    def as_dict(self) -> dict:
        """ Convert object to dictionary """
        return model_as_dict(self)


class TimestampMixin:
    """ Mixin to add update_at and created_at columns
    The columns are added at the *end* of the table
    """
    @declared_attr
    def updated_at(self):
        """ Last update timestamp """
        column = sqlalchemy.Column(
            sqlalchemy.DateTime(timezone=True),
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
        )
        # pylint: disable=protected-access
        column._creation_order = 9800
        return column

    @declared_attr
    def created_at(self):
        """ Creation timestamp """
        column = sqlalchemy.Column(
            sqlalchemy.DateTime(timezone=True),
            default=datetime.utcnow,
            nullable=False,
        )
        # pylint: disable=protected-access
        column._creation_order = 9900
        return column


class DefaultMixin(ObjectIdMixin, TimestampMixin, DictMixin, CreateMixin):
    """ *everything* mixin """
