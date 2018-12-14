import pytest

from flask import request

from hev.auth import is_authorized
from hev.exceptions import NotAuthorized


def test_auth_missing_header(app):
    # ensure the Authorization layer raises NotAuthorized if no 
    # 'Authorization' header is present
    with pytest.raises(NotAuthorized):
        is_authorized(request, None)

def test_auth_wrong_bearer_token(app):
    # ensure the Authorization layer raises NotAuthorized if the Bearer token is wrong
    with app.test_request_context(environ_base={"HTTP_AUTHORIZATION": "Bearer wrong_token"}):
        with pytest.raises(NotAuthorized):
            is_authorized(request, "good_token")

def test_auth_missing_bearer_token(app):
    # ensure the Authorization layer raises NotAuthorized if 'Authorization'
    # does not contain a Bearer token
    with app.test_request_context(environ_base={"HTTP_AUTHORIZATION": "something_else"}):
        with pytest.raises(NotAuthorized):
            is_authorized(request, "good_token")

def test_auth_success(app):
    # ensure the Authorization layer returns True in case of success
    with app.test_request_context(environ_base={"HTTP_AUTHORIZATION": "Bearer good_token"}):
        assert is_authorized(request, "good_token") is True
