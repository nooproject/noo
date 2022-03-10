from __future__ import annotations

from pathlib import Path

from requests import get
from yaml import safe_load

from ..models import Noofile
from .echo import echo


class Resolver:
    def __init__(self) -> None:
        pass

    def resolve_local(self, file: str) -> Noofile:
        path = Path(file)

        if not path.exists():
            raise ValueError(f"No such file: {path}")

        data = safe_load(path.read_text())

        if (ver := data.get("noo_version", 1)) != 2:
            echo(f"Specified noofile cannot be run by this Noo version (local: 2, noofile: {ver})")
            exit(1)

        return Noofile(**data)

    def resolve_http(self, path: str) -> Noofile:
        data = get(path)

        if data.status_code != 200:
            raise ValueError(f"Invalid response looking up noofile: {data.status_code}")

        return Noofile(**safe_load(data.content))

    def resolve_auto(self, loc: str) -> Noofile:
        if loc.startswith("http"):
            return self.resolve_http(loc)

        return self.resolve_local(loc)
