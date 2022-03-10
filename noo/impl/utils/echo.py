from typer import echo as _echo

_quiet = False


def set_quiet() -> None:
    global _quiet
    _quiet = True


def echo(message: str, *, force: bool = False) -> None:
    if _quiet and not force:
        return
    _echo(message)
