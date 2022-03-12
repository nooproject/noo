from pathlib import Path
from shutil import rmtree
from typing import Optional

from typer import Typer

from ..impl.core import NooCore
from ..impl.packager import Packager
from ..impl.registry import REGISTRY
from ..impl.utils import NooException, cancel, echo, set_quiet
from .components import config_app, registry_app

app = Typer()

app.add_typer(registry_app, name="reg")
app.add_typer(config_app, name="conf")


@app.command("clone")
def clone(
    name: str, ref: str, dest: str = ".", shell: bool = False, index: Optional[str] = None, quiet: bool = False
) -> None:
    if quiet:
        set_quiet()

    path = Path(dest) / name

    if path.exists():
        cancel("clone", f"Path {path} already exists.", exc=False)

    if index:
        REGISTRY.set_index(index)

    noofile = REGISTRY.fetch_full(ref)

    echo(f"Cloning project {noofile.name} to {path}...")

    try:
        core = NooCore(REGISTRY, shell)
        core.check(ref)
        core.clone(name, noofile, path)

        echo(f"Done!\n  cd {path}")
    except NooException:
        pass
    except Exception as e:
        echo(f"An error occurred while cloning: {e}")
        rmtree(path)


@app.command("mod")
def mod(ref: str, dest: str = ".", shell: bool = False, index: Optional[str] = None, quiet: bool = False) -> None:
    if quiet:
        set_quiet()

    path = Path(dest)

    if not path.exists():
        cancel("mod", f"Path {path} does not exist.", exc=False)

    if index:
        REGISTRY.set_index(index)

    noofile = REGISTRY.fetch(ref)

    echo(f"Modifying project with {ref}...")

    try:
        core = NooCore(REGISTRY, shell)
        core.check(ref)
        core.mod(noofile, path)
    except NooException:
        pass

    echo(f"Done!")


@app.command("autopackage")
def autopackage(path: str = ".", dest: str = "./noofile.yml", quiet: bool = False) -> None:
    if quiet:
        set_quiet()

    _path = Path(path)
    _dest = Path(dest)

    if _dest.exists():
        cancel("pkg", f"File {_dest} already exists.", exc=False)

    echo(f"Autopacking {_path} to {_dest}...")

    packager = Packager(_path)
    packager.package(_dest)

    echo(f"Done!")
