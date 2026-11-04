import pytest


@pytest.fixture
def unit_client(test_app):

    with test_app.test_client() as client:
        yield client
