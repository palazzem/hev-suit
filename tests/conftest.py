import pytest

from flask import Flask


@pytest.fixture
def app():
    """Fixture: empty application"""
    return Flask(__name__)
