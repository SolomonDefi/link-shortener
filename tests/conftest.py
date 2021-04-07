"""
Set up pytest environment
"""

import os
import pytest
import sqlalchemy as sa
from flask_migrate import Migrate, upgrade
from dotenv import load_dotenv

from application import create_app


def run_tests(args):
    pytest.main(args)


def db_setup():
    """
    Create a fresh test database. Drop the old one if necessary

    Args:
        drop: Whether or not to drop the previous test database

    Returns:
        The URI used to create the database
    """
    db_name = os.getenv('test_db_name', 'test.db')
    test_db_uri = f'sqlite:///{db_name}'

    engine = sa.create_engine(test_db_uri)
    meta = sa.MetaData()
    meta.reflect(engine)
    meta.drop_all(engine)

    return test_db_uri


@pytest.fixture(scope='session')
def app():  # pylint: disable=redefined-outer-name
    """An app for testing"""
    load_dotenv(dotenv_path='env/debug.env')
    db_uri = db_setup()
    shortener_app = create_app(
        config_override={
            'host': '0.0.0.0',
            'SQLALCHEMY_DATABASE_URI': db_uri,
        }
    )

    with shortener_app.app_context():
        Migrate(shortener_app, shortener_app.db)
        upgrade()

    yield shortener_app

    with shortener_app.app_context():
        shortener_app.db.engine.dispose()


@pytest.fixture
def client(app):  # pylint: disable=redefined-outer-name
    """
    A test client for the app
    """
    return app.test_client()
