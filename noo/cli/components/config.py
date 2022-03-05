from typer import Typer, echo

from ...impl.utils import STORE

app = Typer()


ALLOWED_KEYS = {"shell"}


@app.command("set")
def set(key: str, value: str) -> None:
    if key not in ALLOWED_KEYS:
        echo(f"Invalid key: {key}")

    if key == "shell":
        if value not in {"allow", "deny"}:
            echo(f"Invalid value: {value} (must be one of 'allow', 'deny')")
            return

        STORE[key] = value

    echo(f"Set {key} to {value}")


@app.command("reset")
def reset(key: str) -> None:
    if key not in ALLOWED_KEYS:
        echo(f"Invalid key: {key}")

    del STORE[key]

    echo(f"Reset {key}")
