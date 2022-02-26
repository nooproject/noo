from __future__ import annotations

from datetime import datetime
from typing import Optional

from ..models import ReadVariable


def get_variables(name: Optional[str] = None) -> dict[str, dict[str, str | int]]:
    data = {}

    now = datetime.now()

    data["var"] = {}
    data["noo"] = {
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second,
    }

    if name:
        data["noo"]["name"] = name  # type: ignore

    return data


def read_variables(variables: list[ReadVariable]) -> dict[str, str | int]:
    data = {}

    for variable in variables:
        extra = ""
        if variable.default is not None:
            extra = f" [{variable.default}]"

        value = input((variable.prompt or f"Enter {variable.name}") + f"{extra}: ")

        data[variable.name] = value if value else variable.default

    return data
