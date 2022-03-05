from __future__ import annotations

from json import loads
from pathlib import Path

from ..models import Noofile
from .resolver import Resolver
from .store import STORE


class Registry:
    def __init__(self) -> None:
        self._data: dict = STORE.get("registry") or {}
        self._resolver = Resolver()

    def _write(self) -> None:
        STORE["registry"] = self._data

    def _add_local(self, name: str, path: Path) -> None:
        self._data[name] = {
            "type": "local",
            "ref": str(path.absolute()),
        }

        self._write()

    def _add_remote(self, name: str, ref: str) -> None:
        self._data[name] = {
            "type": "remote",
            "ref": ref,
        }

        self._write()

    def _resolve(self, ref: str, remote: bool) -> Noofile:
        if remote:
            return self._resolver.resolve_http(ref)
        return self._resolver.resolve_local(ref)

    def add(self, name: str, ref: str) -> None:
        if ref.startswith(("http://", "https://")):
            self._add_remote(name, ref)
        else:
            self._add_local(name, Path(ref))

    def get(self, name: str) -> Noofile:
        if item := self._data.get(name):
            return self._resolve(item["ref"], item["type"] == "remote")

        for registry in STORE.get("registries") or []:
            if item := registry.get(name):
                return self._resolve(item["ref"], item["type"] == "remote")

        if name.startswith(("http://", "https://")):
            return self._resolve(name, True)

        try:
            return self._resolve(name, False)
        except ValueError:
            raise ValueError(f"No such noofile: {name}")

    def remove(self, name: str) -> None:
        del self._data[name]

        self._write()

    def all(self) -> dict[str, dict[str, str]]:
        return self._data
