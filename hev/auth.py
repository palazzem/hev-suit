from .exceptions import NotAuthorized


def is_authorized(request, authorized_token):
    """Return if the given request is authorized.

    A request is considered authorized to access the functionalities
    offered by HEV suit if it includes a Bearer token in transmitted
    headers.

    Expected format is `Authorization: Bearer <TOKEN>`.

    Args:
        request: A Flask Request object
        authorized_token: A Bearer token considered valid

    Returns:
        A boolean where ``True`` means the request is authorized

    Raises:
        NotAuthorized: An error occurred when the request is not
            authorized. It's raised when a Bearer token is missed
            or is wrong.
    """
    auth_header = request.headers.get("Authorization")

    # do something only if request contains a Bearer token
    if (
        auth_header is None
        or not auth_header.startswith("Bearer")
        or auth_header[7:] != authorized_token
    ):
        raise NotAuthorized("Authorization headers are missing")

    return True
