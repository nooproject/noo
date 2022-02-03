from pathlib import Path
from shutil import rmtree

from typer import Typer

from .impl.loader import load_local
from .impl.runner import run

app = Typer()


@app.command(name="clone")
def clone(name: str, ref: str, dest: str = ".") -> None:
    path = Path(dest) / name

    if ref.startswith("http"):
        raise NotImplementedError("Remote cloning not implemented yet.")

    try:
        data = load_local(Path(ref))
        run(data, path, name)
    except Exception:
        # rmtree(path)
        raise


@app.command(name="init")
def init(quiet: bool = False) -> None:
    pass
