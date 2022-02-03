from datetime import datetime


def _type(d: dict) -> dict[str, str]:
    return {k: str(v) for k, v in d.items()}


def populate() -> dict[str, dict[str, str]]:
    now = datetime.now()

    return {
        "noo": _type(
            {
                "year": now.year,
                "month": now.month,
                "day": now.day,
                "hour": now.hour,
                "minute": now.minute,
                "second": now.second,
            }
        ),
        "var": {},
    }
