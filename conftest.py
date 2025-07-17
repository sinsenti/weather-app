import pytest
from app import app as flask_app


# Foundating to the flask app testing
@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
