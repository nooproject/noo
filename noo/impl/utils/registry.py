from __future__ import annotations

from pathlib import Path

from .storage import Storage


class Registry(Storage):
    def __init__(self) -> None:
        super().__init__("registry")

    def __setitem__(self, key: str, ref: str | Path) -> None:
        if isinstance(ref, Path):
            absolute_ref = "file:" + str(ref.absolute())
        else:
            absolute_ref = ref

        super().__setitem__(key, absolute_ref)

    def __getitem__(self, key: str) -> str | Path:
        ref = super().__getitem__(key)
        if ref.startswith("file:"):
            return Path(ref[5:])
        return ref

    def get(self, key: str) -> str | Path | None:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None
