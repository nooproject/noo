from pathlib import Path
from shutil import rmtree

from typer import Typer, echo

from .components import registry_app
from .components.registry import reg
from ..impl.core import NooCore

app = Typer()

app.add_typer(registry_app, name="reg")


@app.command("clone")
def clone(name: str, ref: str, dest: str = ".") -> None:
    path = Path(dest) / name

    if path.exists():
        echo(f"Path {path} already exists.")
        return

    try:
        abs_ref = reg.get_item(ref)
    except KeyError:
        abs_ref = ref

    echo(f"Cloning project {abs_ref} to {path}...")

    try:
        core = NooCore()
        core.clone(name, str(abs_ref), path)

        echo(f"Done!\n  cd {path}")
    except Exception as e:
        echo(f"An error occurred while cloning: {e}")
        # rmtree(path)
