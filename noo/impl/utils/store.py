from __future__ import annotations

from json import dumps, loads
from os import getenv
from pathlib import Path
from typing import Any

if _base := getenv("NOO_CONFIG_PATH"):
    CONFIG_BASE = Path(_base)
else:
    CONFIG_BASE = Path.home() / ".config" / "noo"

CONFIG_BASE.mkdir(parents=True, exist_ok=True)

del _base


class Store:
    def __init__(self, file: str) -> None:
        self._file = CONFIG_BASE / file

        if self._file.exists():
            self._data = loads(self._file.read_text())
        else:
            self._file.touch()
            self._data = {}

            self._write()

    def _write(self) -> None:
        self._file.write_text(dumps(self._data, indent=2))

    def get(self, key: str) -> Any | None:
        return self._data.get(key)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._write()

    def delete(self, key: str) -> None:
        del self._data[key]
        self._write()

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._write()

    def __delitem__(self, key: str) -> None:
        del self._data[key]
        self._write()


STORE = Store("config.json")
