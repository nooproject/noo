from __future__ import annotations

from pathlib import Path
from random import choices
from shutil import rmtree
from string import ascii_letters

from ..models import BaseNoofile, CommandAction, Noofile, RemoteAction
from ..packager import Packager
from ..registry import Registry
from ..resolvers import clone_github, clone_local
from ..utils import STORE, cancel, echo
from .runner import Runner
from .variables import get_variables, read_variables


class NooCore:
    def __init__(self, registry: Registry, allow_shell: bool = False) -> None:
        self.registry = registry
        self.shell = STORE.get("shell", "deny") == "allow" or allow_shell

        self._noofiles: dict[str, BaseNoofile] = {}

    def check(self, ref: str) -> list[BaseNoofile]:
        noofiles: list[BaseNoofile] = []
        noofile = self.registry.fetch(ref)

        self._noofiles[ref] = noofile

        noofiles.append(noofile)

        for step in noofile.steps:
            for action in step.actions:
                if isinstance(action, RemoteAction):
                    noofiles.extend(self.check(action.remote))
                elif isinstance(action, CommandAction):
                    if action.fail and not self.shell:
                        cancel(
                            "core",
                            f"Noofile with ref {ref} has a command action that requires shell access, but shell is not enabled.",
                        )

        return noofiles

    def clone(self, name: str, spec: Noofile, dest: Path) -> None:
        echo(f"Starting clone process for {spec.name}.")

        if spec.remote.startswith("git:"):
            clone_github(spec.remote[4:], dest)
        elif spec.remote.startswith("file:"):
            clone_local(Path(spec.remote[5:]), dest)
        else:
            cancel("core", f"Invalid remote: {spec.remote}")

        variables = get_variables(name)
        variables["var"].update(read_variables(spec.read))

        runner = Runner(self.mod, dest, spec.name, spec.steps, variables, self.shell)
        runner.run()

    def autoclone(self, name: str, repo: str, dest: Path) -> None:
        echo(f"Starting autoclone process for {repo}.")

        path = Path("/tmp/" + "".join(choices(ascii_letters, k=24)))
        clone_github(repo, path)

        packager = Packager(path)
        noofile = packager.get_noofile(f"git:{repo}")

        noofile_loc = path / "NOO_AUTOCLONE.noofile.yml"
        packager.package(noofile_loc, f"file:{path.absolute()}")

        self.check(str(noofile_loc.absolute()))

        try:
            self.clone(name, noofile, dest)
        finally:
            rmtree(path)

    def mod(
        self,
        noofile: str | BaseNoofile,
        dest: Path,
        default_variables: dict[str, dict[str, str | int]] | None = None,
        in_action: bool = False,
    ) -> None:
        if isinstance(noofile, str):
            spec = self.registry.fetch(noofile)
        else:
            spec = noofile

        if not in_action:
            echo(f"Starting modification for {spec.name or 'unnamed'}.")

        variables = default_variables or get_variables()
        variables["var"].update(read_variables(spec.read))

        runner = Runner(self.mod, dest, spec.name, spec.steps, variables, self.shell)
        runner.run()
