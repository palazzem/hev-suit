def as_bool(v):
    """Convert the given string in a Boolean value.

    Args:
        string: the string that should be converted in boolean

    Returns:
        The boolean converted value for the given string
    """
    return str(v).lower() in ("true", "1")
