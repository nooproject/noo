from pathlib import Path

from typer import echo

from .format import replace
from .noofile import Noofile, ReplaceAction
from .resolvers import clone_github, clone_local
from .variables import populate


def run(noofile: Noofile, dest: Path, name: str) -> None:
    echo(f"Cloning {noofile.name} to {dest}...")

    if noofile.remote.startswith("file:"):
        src = Path(noofile.remote[5:])
        clone_local(src, dest)
    elif noofile.remote.startswith("github:"):
        repo = noofile.remote[7:]
        clone_github(repo, dest)
    else:
        raise NotImplementedError(f"Unknown remote: {noofile.remote}")

    variables = populate()
    variables["noo"]["name"] = name

    for var in noofile.read:
        default = f" [{var.default}]" if var.default else ""
        value = input(f"{var.prompt or var.name}{default}: ")

        if not (value or var.default):
            raise ValueError(f"No value for {var.name}")

        variables["var"][var.name] = value or var.default  # type: ignore

    for step in noofile.steps:
        echo(f"Running step {step.name}...")

        for action in step.actions:

            if isinstance(action, ReplaceAction):
                for file in action.files:
                    file = dest / file
                    file.write_text(
                        replace(file.read_text(), action.src, action.dest, variables)
                    )

    echo("Done!")
