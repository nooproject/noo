from json import dumps, loads
from pathlib import Path

from typer import Typer, echo

from ...impl.utils import Registry

app = Typer()

reg = Registry()


@app.command("add")
def add(name: str, ref: str) -> None:
    reg.add(name, ref)

    echo(f"Registered {name} as {ref}")


@app.command("remove")
def remove(name: str) -> None:
    try:
        reg.remove(name)
    except KeyError:
        echo(f"No such key: {name}")
        return

    echo(f"Unregistered {name}")


@app.command("import")
def import_(file: str) -> None:
    data = loads(Path(file).read_text())

    for key, value in data.items():
        reg.add(key, value["ref"])

    echo(f"Imported {len(data)} items")


@app.command("export")
def export(file: str = "export.json") -> None:
    data = reg.all()

    Path(file).write_text(dumps(data, indent=2))

    echo(f"Exported {len(data)} items")
