import json

from flask import url_for
from hev.api import DatadogAPI


def test_webhook_only_post(client):
    # ensure the Cloud Function accepts only POST requests
    resp = client.get(url_for("webhook"))
    assert resp.status_code == 405


def test_webhook_missing_config(client):
    # ensure the Cloud Function fails if the Config is
    # not properly configured
    resp = client.post(url_for("webhook"))
    data = json.loads(resp.data)

    assert data["message"] == "Configuration error"
    assert resp.status_code == 500


def test_webhook_missing_authorization(client, config):
    # ensure the Cloud Function fails if the Authorization header
    # is missing or wrong
    config.dd_api_key = "api_key"
    config.function_name = "test_config"
    config.bearer_token = "good_token"
    resp = client.post(url_for("webhook"))
    data = json.loads(resp.data)

    assert data["message"] == "Not Authorized"
    assert resp.status_code == 401


def test_webhook_wrong_authorization(client, config):
    # ensure the Cloud Function succeed with the right Configuration
    # and Authorization
    config.dd_api_key = "api_key"
    config.function_name = "test_config"
    config.bearer_token = "good_token"
    config.dry_run = True
    resp = client.post(url_for("webhook"), headers=[("Authorization", "Bearer bad_token")])
    data = json.loads(resp.data)

    assert data["message"] == "Not Authorized"
    assert resp.status_code == 401


def test_webhook_success(client, config):
    # ensure the Cloud Function succeed with the right Configuration
    # and Authorization
    config.dd_api_key = "api_key"
    config.function_name = "test_config"
    config.bearer_token = "good_token"
    config.dry_run = True
    resp = client.post(url_for("webhook"), headers=[("Authorization", "Bearer good_token")])
    data = json.loads(resp.data)

    assert data["message"] == "Success"
    assert resp.status_code == 201


def test_webhook_failure_bpm(client, config, monkeypatch):
    # ensure the Cloud Function returns a Service Unavailable if Datadog
    # dependency doesn't work because of some backend issues
    def mock_response(*args, **kwargs):
        return False
    monkeypatch.setattr(DatadogAPI, "send_bpm", mock_response)

    config.dd_api_key = "api_key"
    config.function_name = "test_config"
    config.bearer_token = "good_token"
    config.dry_run = True

    resp = client.post(url_for("webhook"), headers=[("Authorization", "Bearer good_token")])
    data = json.loads(resp.data)

    assert data["message"] == "Failed"
    assert resp.status_code == 503
