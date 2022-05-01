""" Settings """
import os

from starlette.config import Config
from starlette.datastructures import Secret, URL

VERSION = "2023.4.28"

LOG_FORMAT = "[%(asctime)s] %(levelname)s " \
             "[%(name)s.%(funcName)s:%(lineno)d] %(message)s"
LOG_DATEFMT = "%Y-%m-%dT%H:%M:%S"

config = Config(".env")  # pylint: disable=invalid-name
LOG_LEVEL = config("LOG_LEVEL", default="INFO")
LOG_PATH = config("LOG_PATH", default=None)
LOG_BACKUP_COUNT = config("LOG_BACKUP_COUNT", default=5)
LOG_MAX_BYTES = config("LOG_MAX_BYTES", default=10*1024*1024)


SECRET = config("SECRET", cast=Secret)
ROOT_PATH = config("ROOT_PATH", default="")
HUBSPOT_API_KEY = config("HUBSPOT_API_KEY", default="")
BROWSER_IP = config("BROWSER_IP", default="137.184.183.28")
MAX_EMAILS_PER_DAY = config("MAX_EMAILS_PER_DAY", default=1000, cast=int)
SENDER = config("SENDER")

DATABASE_URL = config("DATABASE_URL", cast=URL)
MYSQL_ROOT_PASSWORD = config("MYSQL_ROOT_PASSWORD", default=None)
if MYSQL_ROOT_PASSWORD:
    DATABASE_URL = DATABASE_URL.replace(
        username="root", password=MYSQL_ROOT_PASSWORD
    )

GOOGLE_USER = config("GOOGLE_USER")
GOOGLE_API_SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.modify"
]

GOOGLE_APPLICATION_CREDENTIALS = config(
    "GOOGLE_APPLICATION_CREDENTIALS", default="service_account.json"
)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
