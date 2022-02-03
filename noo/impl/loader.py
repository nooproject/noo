from pathlib import Path

from yaml import safe_load

from .noofile import Noofile


def load_local(path: Path) -> Noofile:
    data = safe_load(path.read_text())

    return Noofile(**data)
