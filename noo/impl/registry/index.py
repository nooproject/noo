from __future__ import annotations

from hashlib import sha256
from json import JSONDecodeError, loads
from typing import Any, Literal, Optional, TypedDict

from requests import Session
from yaml import safe_load

from ..utils import FileStore, cancel, echo

StaticIndexData = dict[str, dict[str, dict[str, str]]]


class GetIndexResponse(TypedDict):
    type: Literal["static", "dynamic"]
    index: StaticIndexData


class Index:
    def __init__(self, session: Session, url: str) -> None:
        self._session = session
        self._url = url if not url.endswith("/") else url[:-1]
        self._cache = FileStore(f"cache/index/{sha256(url.encode()).hexdigest()}")

    def _fetch_cached(self, url: str) -> Optional[dict[str, Any]]:
        if self._cache.exists(url):
            return safe_load(self._cache.read_text(url))

    def fetch(
        self,
        name: str,
        author: Optional[str] = None,
        version: Optional[str] = None,
        use_cache: bool = True,
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


class StaticIndex:
    def __init__(self, session: Session, url: str, data: StaticIndexData) -> None:
        self._session = session
        self._url = url
        self._data = data

    def fetch(
        self,
        name: str,
        author: Optional[str] = None,
        version: Optional[str] = None,
    ) -> dict[str, Any]:
        """Fetch a raw noofile from a static Noo file index.

        Args:
            name (str): The name of the noofile to fetch.
            author (Optional[str], optional): The author of the noofile. Defaults to None.
            version (Optional[str], optional): The version of the noofile. Defaults to `latest`.

        Returns:
            dict[str, Any]: The raw noofile data
        """

        if author is None:
            author = "_"

        if version is None:
            version = "latest"

        if author not in self._data:
            cancel("index", f"Noofile @{author} not found on index.")

        if name not in self._data[author]:
            cancel("index", f"Noofile @{author}/{name} not found on index.")

        if version not in self._data[author][name]:
            cancel("index", f"Noofile @{author}/{name}:{version} not found on index.")

        res = self._session.get(self._data[author][name][version])

        if res.status_code == 404:
            cancel("index", f"Noofile @{author}/{name}:{version} not found on index {self._url}.")

        res.raise_for_status()

        data = safe_load(res.text)

        return data


def fetch_index(url: str, empty: bool = False) -> Index | StaticIndex:
    """Fetch an index.

    Args:
        url (str): The URL of the index.

    Returns:
        Index | StaticIndex: The index.
    """

    session = Session()

    try:
        res = session.get(url)
    except Exception:
        if empty:
            echo(f"No index found at {url} but continuing with an empty index.")
            return StaticIndex(session, url, {})
        cancel("index", f"Could not fetch index {url}.")

    if res.status_code != 200:
        if empty:
            echo(f"No index found at {url} but continuing with an empty index.")
            return StaticIndex(session, url, {})
        cancel("index", f"Index {url} not found.")

    try:
        data: GetIndexResponse = loads(res.text)
    except JSONDecodeError:
        if empty:
            echo(f"No index found at {url} but continuing with an empty index.")
            return StaticIndex(session, url, {})
        cancel("index", f"Index {url} not valid.")

    if data["type"] == "static":
        return StaticIndex(session, url, data["index"])

    return Index(session, url)
