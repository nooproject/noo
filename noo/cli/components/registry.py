from json import dumps, loads
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
    if ref.startswith("http://") or ref.startswith("https://"):
        reg.set_item(name, ref)
    else:
        reg.set_item(name, Path(ref))

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
    data = loads(Path(file).read_text())

    for key, value in data.items():
        reg.set_item(key, str(Path(value).absolute()))

    echo(f"Imported {len(data)} items")


@app.command("export")
def export(file: str = "export.json") -> None:
    data = reg.read()

    Path(file).write_text(dumps(data, indent=2))

    echo(f"Exported {len(data)} items")
