import logging

from os import getenv

from .utils import as_bool
from .exceptions import ConfigException


class Config(object):
    """Config class used to store the environment configuration for
    this Cloud Function execution.
    """

    MANDATORY_ATTRIBUTES = ["dd_api_key", "function_name", "bearer_token"]

    def __init__(self):
        """Initialize the Config instance using environment variables."""
        self.dd_api_key = getenv("DD_API_KEY")
        self.function_name = getenv("FUNCTION_NAME")
        self.bearer_token = getenv("BEARER_TOKEN")
        self.dry_run = as_bool(getenv("DRY_RUN", False))

    def validate(self):
        """Validate the configuration instance.

        Returns:
            A boolean if the environment is properly configured.

        Raises:
            ConfigException: An error occurred when initializing the
                environment. Mostly related to missing environment
                variables.
        """
        bail_out = False
        for attr in self.MANDATORY_ATTRIBUTES:
            if getattr(self, attr, None) is None:
                bail_out = True
                logging.error(
                    "Environment variable '{}' is not set".format(attr.upper())
                )

        if bail_out:
            raise ConfigException("Mandatory environment variables are not set")
