from . import auth

from .api import DatadogAPI
from .config import Config


conf = Config()

__all__ = [
    "auth",
    "conf",
    "DatadogAPI",
]
