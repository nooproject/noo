from typing import NoReturn

from .echo import echo


class NooException(Exception):
    pass


def cancel(scope: str, reason: str, exc: bool = True) -> NoReturn:
    echo(f"[{scope}] {reason}")

    if not exc:
        exit(1)

    raise NooException(reason)
