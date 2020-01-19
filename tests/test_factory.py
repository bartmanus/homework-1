import pytest

from homework import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
    assert create_app({'STARTUP_COALESCING_SECONDS': 5}) is not None
    assert create_app({'STARTUP_COALESCING_SECONDS': 15}) is not None
    with pytest.raises(ValueError):
        create_app({'STARTUP_COALESCING_SECONDS': 4})
    with pytest.raises(ValueError):
        create_app({'STARTUP_COALESCING_SECONDS': 16})

