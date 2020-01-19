import pytest
from homework import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'testing',
        'STARTUP_COALESCING_SECONDS': 13,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()

