""" Base classes for other models """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE = declarative_base()
Session = sessionmaker()
