from __future__ import annotations

from pathlib import Path

from typer import echo

from .resolver import Resolver
from .runner import Runner
from .variables import get_variables, read_variables
from ..resolvers import clone_github, clone_local


class NooCore:
    def __init__(self) -> None:
        self.resolver = Resolver()

    def clone(self, name: str, noofile: str, dest: Path) -> None:
        spec = self.resolver.resolve(noofile)

        echo(f"Starting clone process for {spec.name or name}.")

        if spec.remote.startswith("git:"):
            clone_github(spec.remote[4:], dest)
        elif spec.remote.startswith("file:"):
            clone_local(Path(spec.remote[5:]), dest)
        else:
            raise ValueError(f"Invalid remote: {spec.remote}")

        variables = get_variables(name)
        variables["var"].update(read_variables(spec.read))

        echo(f"Cloned to {dest.absolute()}.")

        runner = Runner(dest, spec.steps, variables)
        runner.run()
