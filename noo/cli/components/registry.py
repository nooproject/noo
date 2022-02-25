from os import getenv
from pathlib import Path

from typer import Typer, echo

from ...impl.utils import Registry

app = Typer()


rpath = None
if _path := getenv("NOO_REGISTRY_PATH"):
    rpath = Path(_path)

del _path

reg = Registry(rpath)

del rpath


@app.command("add")
def add(name: str, ref: str) -> None:
    reg.set_item(name, ref)

    echo(f"Registered {name} as {ref}")


@app.command("remove")
def remove(name: str) -> None:
    try:
        reg.del_item(name)
    except KeyError:
        echo(f"No such key: {name}")
        return

    echo(f"Unregistered {name}")


@app.command("import")
def import_(file: str) -> None:
    echo(f"Importing registries is not yet implemented.")


@app.command("export")
def export(file: str = "export.json") -> None:
    echo(f"Exporting registries is not yet implemented.")
