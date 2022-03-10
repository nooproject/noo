from __future__ import annotations

from pathlib import Path
from typing import Any

from yaml import safe_load


def fetch_local(path: Path) -> dict[str, Any]:
    return safe_load(path.read_text())
