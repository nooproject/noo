from typing import NoReturn

from typer import echo


class NooException(Exception):
    pass


def cancel(scope: str, reason: str) -> NoReturn:
    echo(f"[{scope}] {reason}")

    raise NooException(reason)
