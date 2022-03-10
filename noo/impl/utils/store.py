from __future__ import annotations

from json import dumps, loads
from os import getenv
from pathlib import Path
from typing import Any

if _base := getenv("NOO_CONFIG_PATH"):
    CONFIG_BASE = Path(_base)
else:
    CONFIG_BASE = Path.home() / ".config" / "noo"  # type: ignore

CONFIG_BASE.mkdir(parents=True, exist_ok=True)

del _base


class Store:
    def __init__(self, file: str) -> None:
        self._file = CONFIG_BASE / file

        if self._file.exists():
            self._data = loads(self._file.read_text())
        else:
            self._file.touch()
            self._data: dict[str, Any] = {}

            self._write()

    def _write(self) -> None:
        self._file.write_text(dumps(self._data, indent=2))

    def get(self, key: str, default: Any | None = None) -> Any | None:
        return self._data.get(key, default)

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


class FileStore:
    def __init__(self, path: str) -> None:
        self._path = CONFIG_BASE / path

        if not self._path.exists():
            self._path.mkdir(parents=True)

    def exists(self, file: str) -> bool:
        return (self._path / file).exists()

    def write(self, file: str, value: str | bytes) -> None:
        if isinstance(value, str):
            (self._path / file).write_text(value)
        else:
            (self._path / file).write_bytes(value)

    def read_text(self, file: str) -> str:
        return (self._path / file).read_text()

    def read_bytes(self, file: str) -> bytes:
        return (self._path / file).read_bytes()

    def absolute(self, file: str) -> str:
        return str((self._path / file).absolute())

    def delete(self, file: str) -> None:
        (self._path / file).unlink()


STORE = Store("config.json")
