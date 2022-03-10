from __future__ import annotations

from typing import Any

from requests import Session
from yaml import safe_load

from ..utils import cancel


class RemoteResolver:
    def __init__(self) -> None:
        self._session = Session()

    def fetch(self, ref: str) -> dict[str, Any]:
        res = self._session.get(ref)

        if res.status_code == 404:
            cancel("registry", f"Ref {ref} not found.")

        res.raise_for_status()

        return safe_load(res.text)
