from __future__ import annotations

from pathlib import Path

from typer import echo

from ..resolvers import clone_github, clone_local
from .resolver import Resolver
from .runner import Runner
from .variables import get_variables, read_variables


class NooCore:
    def __init__(self, allow_shell: bool = False) -> None:
        self.resolver = Resolver()
        self.shell = allow_shell

    def clone(self, name: str, noofile: str, dest: Path) -> None:
        spec = self.resolver.resolve(noofile)

        echo(f"Starting clone process for {spec.name or name}.")

        if not spec.remote:
            echo(f"No remote specified for {spec.name or name}")
            return

        if spec.remote.startswith("git:"):
            clone_github(spec.remote[4:], dest)
        elif spec.remote.startswith("file:"):
            clone_local(Path(spec.remote[5:]), dest)
        else:
            raise ValueError(f"Invalid remote: {spec.remote}")

        variables = get_variables(name)
        variables["var"].update(read_variables(spec.read))

        runner = Runner(self, dest, spec.steps, variables, self.shell)
        runner.run()

    def mod(self, noofile: str, dest: Path) -> None:
        spec = self.resolver.resolve(noofile)

        echo(f"Starting modification for {spec.name or 'unnamed'}.")

        variables = get_variables()
        variables["var"].update(read_variables(spec.read))

        runner = Runner(self, dest, spec.steps, variables, self.shell)
        runner.run()
