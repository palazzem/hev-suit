import os
import pytest

from hev.config import Config
from hev.exceptions import ConfigException


def test_config_init():
    # ensure the Configuration has set attributes used
    # in the application
    config = Config()
    assert config.dd_api_key is None
    assert config.function_name is None
    assert config.bearer_token is None

def test_mandatory_attributes():
    # ensure critical attributes are mandatory; there is
    # no reason to update this test unless you want to
    # be sure the field is never removed from the list of
    # mandatory fields
    assert "dd_api_key" in Config.MANDATORY_ATTRIBUTES
    assert "function_name" in Config.MANDATORY_ATTRIBUTES
    assert "bearer_token" in Config.MANDATORY_ATTRIBUTES

def test_config_init_with_envs(monkeypatch):
    # ensure the Config object is initialized with environment variables
    monkeypatch.setitem(os.environ, "DD_API_KEY", "api_key")
    monkeypatch.setitem(os.environ, "FUNCTION_NAME", "test_config")
    monkeypatch.setitem(os.environ, "BEARER_TOKEN", "bearer_token")
    config = Config()
    assert config.dd_api_key == "api_key"
    assert config.function_name == "test_config"
    assert config.bearer_token == "bearer_token"

def test_config_validate_exception():
    # ensure a not configured environment doesn't pass Config validation
    config = Config()

    with pytest.raises(ConfigException) as excinfo:
        config.validate()