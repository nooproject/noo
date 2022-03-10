from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from typer import Typer

from ...impl.utils import cancel

app = Typer()


@app.command("generate")
def generate(directory: str = ".", suffix: str = ".noofile.yml", remote: Optional[str] = None) -> None:
    path = Path(directory)

    if not path.exists():
        cancel("collection", "The specified directory does not exist.", exc=False)

    if not path.is_dir():
        cancel("collection", "The specified path is not a directory.", exc=False)

    files: List[Path] = []

    for file in path.iterdir():
        if not file.is_file():
            continue

        if not file.name.endswith(suffix):
            continue

        files.append(file)

    if not files:
        cancel("collection", "No noofiles found.", exc=False)

    commands: list[str] = []

    branch = "master"

    if remote and "@" in remote:
        remote, branch = remote.split("@")

    for file in files:
        name = file.name.split(".")[0]

        if remote:
            commands.append(f"noo reg add {name} https://raw.githubusercontent.com/{remote}/{branch}/{str(file)}")
        else:
            commands.append(f"noo reg add {name} {str(file)}")

    Path("register.sh").write_text("\n".join(commands))
