from pathlib import Path
from shutil import rmtree

from typer import Typer, echo

from .impl.loader import load_local
from .impl.runner import run
from .registry import load, save

app = Typer()


@app.command(name="clone")
def clone(name: str, ref: str, dest: str = ".") -> None:
    path = Path(dest) / name

    if ref.startswith("http"):
        raise NotImplementedError("Remote cloning not implemented yet.")

    try:
        if ref.startswith("r:"):
            ref = load()[ref[2:]]
        data = load_local(Path(ref))
        run(data, path, name)
    except Exception:
        rmtree(path)
        raise


@app.command(name="init")
def init(quiet: bool = False) -> None:
    pass


@app.command(name="register")
def register(name: str, ref: str) -> None:
    save(name, ref)

    echo(f"Registered {name} as {ref}")
