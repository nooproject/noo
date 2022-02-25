from __future__ import annotations

from json import dumps, loads
from pathlib import Path
from typing import Optional


class Registry:
    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = path or Path.home() / ".config" / "noo"
        self.path.mkdir(parents=True, exist_ok=True)

        self.value = self.read(cache=False)

    def read(self, cache: bool = True) -> dict[str, str]:
        path = self.path / "registry.json"

        if not path.exists():
            return {}

        data = loads(path.read_text())

        if cache:
            self.value = data

        return data

    def write(self) -> None:
        path = self.path / "registry.json"

        if not path.exists():
            path.touch()

        path.write_text(dumps(self.value, indent=2))

    def set_item(self, key: str, ref: str | Path) -> None:
        if isinstance(ref, Path):
            absolute_ref = "file:" + str(ref.absolute())
        else:
            absolute_ref = ref

        self.value[key] = absolute_ref

        self.write()

    def get_item(self, key: str) -> str | Path:
        ref = self.value[key]

        if ref.startswith("file:"):
            return Path(ref[5:])

        return ref

    def del_item(self, key: str) -> None:
        del self.value[key]
