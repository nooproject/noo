from __future__ import annotations

from json import dumps, loads
from pathlib import Path
from typing import Any


class Storage:
    def __init__(self, storage_name: str) -> None:
        config_path = Path.home() / ".config" / "noo"
        config_path.mkdir(parents=True, exist_ok=True)

        self.path = config_path / (storage_name + ".json")

        self._value: dict[str, Any] | None = None

    def _read(self, cache: bool = False) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        if cache and self._value:
            return self._value

        data = loads(self.path.read_text())
        self._value = data

        return data

    def _write(self) -> None:
        if not self.path.exists():
            self.path.touch()

        self.path.write_text(dumps(self._value, indent=2))

    def __getitem__(self, key: str) -> Any:
        if self._value is None:
            self._read()
            assert self._value is not None
        return self._read()[key]

    def get(self, key: str) -> Any:
        try:
            return self[key]
        except KeyError:
            return None

    def __setitem__(self, key: str, value: Any) -> None:
        if self._value is None:
            self._read()
            assert self._value is not None
        self._value[key] = value
        self._write()

    def __delitem__(self, key: str) -> None:
        if self._value is None:
            self._read()
            assert self._value is not None
        del self._value[key]
        self._write()
