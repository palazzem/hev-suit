import pytest
import logging
import datadog

from flask import request

from hev.api import DatadogAPI, DialogFlowRequest
from hev.constants import KIND_DIASTOLIC, KIND_SYSTOLIC
from hev.exceptions import BadRequest


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


def test_dialog_flow_init(app):
    # ensure a DialogFlow class can parse Flask Request instance
    with app.test_request_context(json={"key": "value"}):
        dialog = DialogFlowRequest(request)
        assert dialog._data == {"key": "value"}


def test_dialog_flow_init_malformed(app):
    # ensure a DialogFlow class can parse Flask Request instance
    with app.test_request_context(data="some_value"):
        dialog = DialogFlowRequest(request)
        assert dialog._data is None


def test_dialog_flow_init_malformed_json(app):
    # ensure a DialogFlow class can parse Flask Request instance
    with app.test_request_context(
        data="not_json_data", content_type="application/json"
    ):
        dialog = DialogFlowRequest(request)
        assert dialog._data is None


def test_dialog_flow_validation(app):
    # ensure a deserialized payload is considered valid
    with app.test_request_context(
        json={"queryResult": {"parameters": {"bpm": 42, "min": 42, "max": 42}}}
    ):
        assert DialogFlowRequest(request).validate() is True


def test_dialog_flow_mandatory_fields(app):
    # ensure some fields are mandatory to pass the validation
    assert DialogFlowRequest.MANDATORY == ["bpm", "min", "max"]


def test_dialog_flow_validation_error(app):
    # ensure a deserialized payload without all the values raises an Exception
    with app.test_request_context(json={"queryResult": {"parameters": {}}}):
        with pytest.raises(BadRequest):
            DialogFlowRequest(request).validate()


def test_dialog_flow_validation_empty(app):
    # ensure an empty payload raises a BadRequest exception
    with app.test_request_context():
        with pytest.raises(BadRequest):
            DialogFlowRequest(request).validate()


def test_dialog_flow_get_parameter(app):
    # ensure a deserialized payload is considered valid
    with app.test_request_context(
        json={"queryResult": {"parameters": {"bpm": 1, "min": 2, "max": 3}}}
    ):
        dialog = DialogFlowRequest(request)
        assert dialog.get_parameter("bpm") == 1
        assert dialog.get_parameter("min") == 2
        assert dialog.get_parameter("max") == 3
