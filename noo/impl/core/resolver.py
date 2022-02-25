from __future__ import annotations

from json import loads
from pathlib import Path

from requests import get
from yaml import safe_load

from ..models import Noofile


class Resolver:
    def __init__(self) -> None:
        pass

    def _resolve_local(self, file: str) -> Noofile:
        path = Path(file)

        if not path.exists():
            raise ValueError(f"No such file: {path}")

        return Noofile(**safe_load(path.read_text()))

    def _resolve_http(self, path: str) -> Noofile:
        data = get(path)

        if data.status_code != 200:
            raise ValueError(f"Invalid response looking up noofile: {data.status_code}")

        return Noofile(**safe_load(data.content))

    def resolve(self, loc: str) -> Noofile:
        if loc.startswith("http"):
            return self._resolve_http(loc)

        return self._resolve_local(loc)
