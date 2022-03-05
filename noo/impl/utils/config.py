from __future__ import annotations

from .storage import Storage


class Config(Storage):
    def __init__(self) -> None:
        super().__init__("config")
