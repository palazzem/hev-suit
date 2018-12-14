import logging

from hev import conf, DatadogAPI, auth
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
    # Validate Environment Configuration
    try:
        conf.validate()
        auth.is_authorized(request, conf.bearer_token)
    except ConfigException as e:
        logging.critical("Unable to configure Cloud Function: %s", str(e))
        return ("Configuration error", 500)
    except NotAuthorized as e:
        # TODO: update the response so that it can be parsed from a
        # Google Action
        logging.critical(str(e))
        return ("Not Authorized", 401)

    # Prepare the API
    api = DatadogAPI(conf.dd_api_key, conf.function_name)

    # Collect values from Cloud Datastore
    # TODO: Static values, NotImplemented
    bpm, value_min, value_max = 70, 80, 144

    # Send HEV parameters to Datadog
    # TODO: check responses and return the right answer to the client
    api.send_bpm(bpm)
    api.send_pressure(value_min, kind=KIND_DIASTOLIC)
    api.send_pressure(value_max, kind=KIND_SYSTOLIC)

    logging.info("Cloud Function executed correctly.")
    return ("Success", 201)
