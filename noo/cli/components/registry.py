from json import dumps, loads
from pathlib import Path

from typer import Typer

from ...impl.registry import REGISTRY
from ...impl.utils import echo

app = Typer()


@app.command("add")
def add(name: str, ref: str) -> None:
    REGISTRY.add(name, ref)

    echo(f"Registered {name} as {ref}")


@app.command("remove")
def remove(name: str) -> None:
    try:
        REGISTRY.remove(name)
    except KeyError:
        echo(f"No such key: {name}")
        return

    echo(f"Unregistered {name}")


@app.command("import")
def import_(file: str) -> None:
    data = loads(Path(file).read_text())

    for key, value in data.items():
        REGISTRY.add(key, value["ref"])

    echo(f"Imported {len(data)} items")


@app.command("export")
def export(file: str = "export.json") -> None:
    data = REGISTRY.all()

    Path(file).write_text(dumps(data, indent=2))

    echo(f"Exported {len(data)} items")
