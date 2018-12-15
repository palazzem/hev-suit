import hev
import json
import logging

from flask import abort

from hev.api import DatadogAPI
from hev.constants import KIND_DIASTOLIC, KIND_SYSTOLIC
from hev.exceptions import ConfigException, NotAuthorized


def entrypoint(request):
    """Cloud Function entrypoint.

    Args:
        request: Flask Request object

    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    # Allow only POST methods
    if request.method != "POST":
        return abort(405)

    # Validate Environment Configuration
    try:
        hev.conf.validate()
        hev.auth.is_authorized(request, hev.conf.bearer_token)
    except ConfigException as e:
        logging.critical("Unable to configure Cloud Function: %s", str(e))
        response = json.dumps({"message": "Configuration error"})
        return (response, 500)
    except NotAuthorized as e:
        # TODO: update the response so that it can be parsed from a
        # Google Action
        logging.critical(str(e))
        response = json.dumps({"message": "Not Authorized"})
        return (response, 401)

    # Prepare the API
    api = DatadogAPI(hev.conf.dd_api_key, hev.conf.function_name, hev.conf.dry_run)

    # Collect values from Cloud Datastore
    # TODO: Static values, NotImplemented
    bpm, value_min, value_max = 70, 80, 144

    # Send HEV parameters to Datadog
    op_1 = api.send_bpm(bpm)
    op_2 = api.send_pressure(value_min, kind=KIND_DIASTOLIC)
    op_3 = api.send_pressure(value_max, kind=KIND_SYSTOLIC)

    # Check all calls were a success
    if op_1 and op_2 and op_3:
        logging.info("Cloud Function executed correctly.")
        response = json.dumps({"message": "Success"})
        status = 201
    else:
        logging.error("Cloud Function executed with errors.")
        response = json.dumps({"message": "Failed"})
        status = 503
    return (response, status)
