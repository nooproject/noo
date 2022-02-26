from pathlib import Path
from typing import Protocol

from ...models import Noofile


class AutoPackagerRunner(Protocol):
    def __init__(self, location: Path) -> None:
        ...

    def package(self, remote: str) -> Noofile:
        ...

    @staticmethod
    def detect(location: Path) -> bool:
        ...
