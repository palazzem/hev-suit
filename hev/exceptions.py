class ConfigException(Exception):
    """ConfigException must be raised when a configuration
    is missing for this Google Cloud Function.
    """

    pass


class NotAuthorized(Exception):
    """NotAuthorized must be raised when a Bearer token
    is not available in the request headers or if it's
    wrong.
    """

    pass


class BadRequest(Exception):
    """BadRequest must be raised when received Flask Request
    contains malformed data.
    """

    pass
