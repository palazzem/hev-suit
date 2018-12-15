import hev
import pytest

from main import create_app
from hev.config import Config


@pytest.fixture
def app():
    """Fixture: empty application"""
    return create_app()


@pytest.fixture
def config():
    """Fixture: Configuration object"""
    # Store boostrap Config
    original = hev.conf

    # Yield a new Config object that replaces the global one
    conf = Config()
    hev.conf = conf
    yield conf

    # Restore bootstrap Config
    hev.conf = original
