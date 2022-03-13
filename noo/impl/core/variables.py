from __future__ import annotations

from datetime import datetime
from re import match
from typing import Optional

from ..models import ReadVariable
from ..utils import cancel

Variables = dict[str, str | int]
NSVariables = dict[str, Variables]


def get_variables(name: Optional[str] = None) -> NSVariables:
    data: NSVariables = {}

    now = datetime.now()

    data["var"] = {}
    data["noo"] = {
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second,
        "isotime": now.isoformat(),
        "unixtime": round(now.timestamp()),
    }

    if name:
        data["noo"]["name"] = name

    return data


def read_variables(variables: list[ReadVariable]) -> Variables:
    data: Variables = {}

    for variable in variables:
        extra = ""
        if variable.default is not None:
            extra = f" [{variable.default}]"

        value = input((variable.prompt or f"Enter {variable.name}") + f"{extra}: ")

        if value == "" and variable.default is None and variable.required:
            raise ValueError(f"{variable.name} is required.")

        value = value or variable.default or ""

        if variable.match is not None:
            if not match(variable.match, value):
                cancel("vars", f"{variable.name} does not match {variable.match}.")

        data[variable.name] = value

    return data
