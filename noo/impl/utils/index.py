from hashlib import sha256
from typing import Optional
from urllib.parse import quote

from requests import get
from typer import echo

from ..models import Noofile
from .resolver import Resolver
from .store import STORE, FileStore


class IndexResolver:
    def __init__(self, resolver: Resolver, index: Optional[str] = None) -> None:
        self.resolver = resolver
        self.index = index or STORE.get("index") or "https://index.nooproject.dev"

        self.store = FileStore("index")
        self.temp = FileStore("temp")

        self.index_type: Optional[str] = None
        self.static_index: Optional[dict[str, str]] = None

    def _resolve_type(self) -> None:
        index = get(self.index)
        index.raise_for_status()

        meta = index.json()

        self.index_type = meta["type"]

        echo(f"Index type resolved as {self.index_type}")

        if self.index_type == "static":
            self.static_index = meta["index"]

    def _fetch_static(self, author: str, name: str, version: str) -> Noofile:
        if self.static_index is None:
            raise ValueError("No static index found.")

        url = self.static_index.get(f"@{author}/{name}:{version}")

        if url is None:
            raise ValueError(f"Noofile @{author}/{name}:{version} not found.")

        return self.resolver.resolve_http(url)

    def _fetch_complex(self, author: str, name: str, version: str) -> Noofile:
        url = f"{self.index}/project/{quote(author)}/{quote(name)}"
        uhash = sha256(f"{url}//{version}".encode("utf-8")).hexdigest()

        if self.store.exists(uhash):
            echo(f"Noofile {uhash} exists locally, using cache.")
            return self.resolver.resolve_local(self.store.absolute(uhash))

        res = get(url, params={"version": version})
        res.raise_for_status()

        data = res.text

        if version != "latest":
            self.store.write(uhash, data)

            return self.resolver.resolve_local(self.store.absolute(uhash))
        else:
            self.temp.write(uhash, data)

            noofile = self.resolver.resolve_local(self.temp.absolute(uhash))

            self.temp.delete(uhash)

            return noofile

    def fetch(self, author: str, name: str, version: str) -> Noofile:
        if self.index_type is None:
            self._resolve_type()

        if self.index_type == "static":
            return self._fetch_static(author, name, version)
        else:
            return self._fetch_complex(author, name, version)
