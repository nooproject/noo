from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from ..models import Noofile
from .index import IndexResolver
from .resolver import Resolver
from .store import STORE


class RegistryEntry(TypedDict):
    type: str
    ref: str


class Registry:
    def __init__(self) -> None:
        self._data: dict[str, RegistryEntry] = STORE.get("registry") or {}
        self._resolver = Resolver()
        self._index = IndexResolver(self._resolver)

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
        if name.startswith("@"):
            name = name[1:]

            author, pkg = name.split("/")
            pkg_data = pkg.split(":")

            if len(pkg_data) == 1:
                pkg_data.append("latest")

            return self._index.fetch(author, *pkg_data)

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

    def all(self) -> dict[str, RegistryEntry]:
        return self._data

    def set_index(self, index: str) -> None:
        self._index = IndexResolver(self._resolver, index)
