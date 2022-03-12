from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from re import compile as re_compile
from typing import Any, Optional

from ..models import BaseNoofile, Noofile
from ..utils import STORE, cancel
from .index import fetch_index
from .local import fetch_local
from .remote import RemoteResolver

INDEX_PACKAGE = re_compile(
    r"^@((?P<author>[a-zA-Z0-9_-]{2,32})\/)?"
    r"(?P<name>[a-zA-Z0-9_-]{1,64})"
    r"(:(?P<version>[a-zA-Z0-9\._-]{1,64}))?$"
)


class Registry:
    def __init__(self) -> None:
        self._index = fetch_index(STORE.get("index") or "https://index.nooproject.dev/api/v1", empty=True)
        self._remote = RemoteResolver()

        self._data: dict[str, str] = STORE.get("registry") or {}

    def _fetch(self, ref: str, _from: Optional[str] = None) -> dict[str, Any]:
        if match := INDEX_PACKAGE.search(ref):
            author = match.group("author")
            name = match.group("name")
            version = match.group("version")

            return self._index.fetch(name, author, version)

        path = Path(ref)

        if path.is_file():
            return fetch_local(path)

        if ref.startswith(("https://", "http://")):
            return self._remote.fetch(ref)

        if data_ref := self._data.get(ref):
            if _from == data_ref:
                cancel("registry", f"Circular dependency detected: {ref}")

            return self._fetch(data_ref, ref)

        cancel("registry", f"Unknown noofile ref: {ref}" + (f" (From: {ref})" * bool(_from)))

    def _save(self) -> None:
        STORE["registry"] = self._data

    @lru_cache(maxsize=None)
    def fetch(self, ref: str) -> BaseNoofile:
        return BaseNoofile(**self._fetch(ref))

    @lru_cache(maxsize=None)
    def fetch_full(self, ref: str) -> Noofile:
        return Noofile(**self._fetch(ref))

    def add(self, name: str, ref: str) -> None:
        if not ref.startswith(("https://", "http://")):
            ref = str(Path(ref).absolute())

        self._data[name] = ref

        self._save()

    def remove(self, name: str) -> None:
        del self._data[name]

        self._save()

    def all(self) -> dict[str, str]:
        return self._data

    def set_index(self, index: str) -> None:
        self._index = fetch_index(index)


REGISTRY = Registry()
