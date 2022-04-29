import pytest

from starlette.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env", usecwd=True))
load_dotenv(find_dotenv(".env.test", usecwd=True), override=True)

# pylint: disable=wrong-import-position
from marketing import settings, models  # noqa
from marketing.main import app  # noqa


@pytest.fixture(scope="function", name="client")
def client_fixture():
    return TestClient(app)


@pytest.fixture(scope="function", name="database")
def database_fixture():
    """
    Create a clean test database every time the tests are run.
    """

    url = str(settings.DATABASE_URL)
    assert url.endswith("_test")

    if database_exists(url):
        drop_database(url)

    engine = create_engine(url)
    create_database(url)
    models.BASE.metadata.create_all(engine)
    yield
    drop_database(url)


@pytest.fixture(scope="function", name="session")
def session_fixture(database):
    session = models.Session()
    yield session
    session.close()
