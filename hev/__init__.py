from . import exceptions

from .config import Config


conf = Config()

__all__ = [
    "conf",
    "exceptions",
]
