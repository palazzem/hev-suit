import logging
import datadog

from hev.api import DatadogAPI
from hev.constants import KIND_DIASTOLIC, KIND_SYSTOLIC


def test_datadog_api_init():
    # ensure the Datadog API is initialized
    api = DatadogAPI("api_key", "test_config")
    assert api._api == datadog.api
    assert api._api._api_key == "api_key"
    assert api._function_name == "test_config"


def test_send_bpm(monkeypatch):
    # ensure the API sends the right BPM values
    def mock_return(*args, **kwargs):
        assert kwargs["host"] == "test_config"
        assert kwargs["metric"] == "hev.parameters.bpm"
        assert kwargs["points"] == 42
        return {"status": "ok"}

    api = DatadogAPI("api_key", "test_config")
    monkeypatch.setattr(api._api.Metric, "send", mock_return)
    status = api.send_bpm(42)

    assert status is True


def test_send_bpm_failure(monkeypatch, caplog):
    # ensure the API logs in case of errors
    def mock_return(*args, **kwargs):
        return {"status": "failure"}

    api = DatadogAPI("api_key", "test_config")
    monkeypatch.setattr(api._api.Metric, "send", mock_return)
    status = api.send_bpm(42)

    assert caplog.record_tuples == [("root", logging.ERROR, "{'status': 'failure'}")]
    assert status is False


def test_send_pressure_min(monkeypatch):
    # ensure the API sends the right min pressure values
    def mock_return(*args, **kwargs):
        assert kwargs["host"] == "test_config"
        assert kwargs["metric"] == "hev.parameters.pressure"
        assert kwargs["points"] == 42
        assert kwargs["tags"] == ["min"]
        return {"status": "ok"}

    api = DatadogAPI("api_key", "test_config")
    monkeypatch.setattr(api._api.Metric, "send", mock_return)
    status = api.send_pressure(42, KIND_DIASTOLIC)

    assert status is True


def test_send_pressure_max(monkeypatch):
    # ensure the API sends the right max pressure values
    def mock_return(*args, **kwargs):
        assert kwargs["host"] == "test_config"
        assert kwargs["metric"] == "hev.parameters.pressure"
        assert kwargs["points"] == 42
        assert kwargs["tags"] == ["max"]
        return {"status": "ok"}

    api = DatadogAPI("api_key", "test_config")
    monkeypatch.setattr(api._api.Metric, "send", mock_return)
    status = api.send_pressure(42, KIND_SYSTOLIC)

    assert status is True


def test_send_pressure_failure(monkeypatch, caplog):
    # ensure the API logs in case of errors
    def mock_return(*args, **kwargs):
        return {"status": "failure"}

    api = DatadogAPI("api_key", "test_config")
    monkeypatch.setattr(api._api.Metric, "send", mock_return)
    status = api.send_pressure(42, KIND_DIASTOLIC)

    assert caplog.record_tuples == [("root", logging.ERROR, "{'status': 'failure'}")]
    assert status is False
