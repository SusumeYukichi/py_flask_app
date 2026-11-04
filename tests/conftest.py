import pytest

from app import create_app
from app.config import TestingConfig
from app.extensions import db


@pytest.fixture
def test_app():

    test_app = create_app(TestingConfig)

    with test_app.app_context():
        db.create_all()

    yield test_app

    with test_app.app_context():
        db.session.remove()
        db.drop_all()
