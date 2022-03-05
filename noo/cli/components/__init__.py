from .collection import app as collection_app
from .config import app as config_app
from .registry import app as registry_app

__all__ = (
    "collection_app",
    "config_app",
    "registry_app",
)
