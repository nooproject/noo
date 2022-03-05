from __future__ import annotations

from pathlib import Path

from typer import echo

from ..models import BaseNoofile, Noofile
from ..resolvers import clone_github, clone_local
from ..utils import STORE, Registry
from .runner import Runner
from .variables import get_variables, read_variables


class NooCore:
    def __init__(self, registry: Registry, allow_shell: bool = False) -> None:
        self.registry = registry
        self.shell = STORE.get("shell", "deny") == "allow" or allow_shell

    def clone(self, name: str, spec: Noofile, dest: Path) -> None:
        echo(f"Starting clone process for {spec.name}.")

        if not spec.remote:
            echo(f"No remote specified for {spec.name}")
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

    def mod(
        self,
        noofile: str | BaseNoofile,
        dest: Path,
        default_variables: dict[str, dict[str, str | int]] | None = None,
        in_action: bool = False,
    ) -> None:
        if isinstance(noofile, str):
            spec = self.registry.get(noofile)
        else:
            spec = noofile

        if not in_action:
            echo(f"Starting modification for {spec.name or 'unnamed'}.")

        variables = default_variables or get_variables()
        variables["var"].update(read_variables(spec.read))

        runner = Runner(self, dest, spec.steps, variables, self.shell)
        runner.run()
