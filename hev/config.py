import logging

from os import getenv

from .api import API


MANDATORY_ENV_VARS = [
    "DD_API_KEY",
    "FUNCTION_NAME",
]


def init():
    """Initializes the Cloud Function with some environment variables.
    This function has as a side-effect the configuration of the
    Datadog API.
    """
    # Ensure the environment is properly configured
    bail_out = False
    for key in MANDATORY_ENV_VARS:
        if getenv(key) is None:
            bail_out = True
            logging.error("Environment variable '{}' is not set.".format(key))

    if bail_out:
        raise RuntimeError("mandatory environment variables are not set.")

    # Configure the environment
    api_key = getenv("DD_API_KEY")
    function_name = getenv("FUNCTION_NAME")

    return API(api_key, function_name)
