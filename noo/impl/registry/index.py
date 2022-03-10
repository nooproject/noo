from __future__ import annotations

from hashlib import sha256
from typing import Any, Optional

from requests import Session
from yaml import safe_load

from ..utils import FileStore, cancel


class Index:
    def __init__(self, url: str) -> None:
        self._url = url if not url.endswith("/") else url[:-1]
        self._session = Session()
        self._cache = FileStore(f"cache/index/{sha256(url.encode()).hexdigest()}")

    def _fetch_cached(self, url: str) -> Optional[dict[str, Any]]:
        if self._cache.exists(url):
            return safe_load(self._cache.read_text(url))

    def fetch(
        self, name: str, author: Optional[str] = None, version: Optional[str] = None, use_cache: bool = True
    ) -> dict[str, Any]:
        """Fetch a raw noofile from a Noo file index.

        Args:
            name (str): The name of the noofile to fetch.
            author (Optional[str], optional): The author of the noofile. Defaults to None.
            version (Optional[str], optional): The version of the noofile. Defaults to `latest`.
            use_cache (bool, optional): Whether to use the cache. Defaults to True.

        Returns:
            dict[str, Any]: The raw noofile data
        """

        if author is None:
            author = "_"

        if version is None:
            version = "latest"

        url = f"{self._url}/project/{author}/{name}/{version}"
        url_hash = sha256(url.encode()).hexdigest()

        if use_cache:
            data = self._fetch_cached(url_hash)

            if data is not None:
                return data

        res = self._session.get(url)

        if res.status_code == 404:
            cancel("index", f"Noofile @{author}/{name}:{version} not found on index {self._url}.")

        res.raise_for_status()

        self._cache.write(url_hash, res.text)
        data = safe_load(res.text)

        return data
