from __future__ import annotations

from pathlib import Path
from subprocess import PIPE, Popen
from typing import TYPE_CHECKING

from typer import echo

from ..models import (
    CommandAction,
    CreateAction,
    DeleteAction,
    RemoteAction,
    RenameAction,
    ReplaceAction,
    Step,
)
from ..utils import RunnerError
from .formatter import format_vars, replace

if TYPE_CHECKING:
    from .core import NooCore

OPMAP = {
    "eq": lambda a, b: str(a) == str(b),
    "ne": lambda a, b: str(a) != str(b),
    "gt": lambda a, b: int(a) > int(b),
    "ge": lambda a, b: int(a) >= int(b),
    "lt": lambda a, b: int(a) < int(b),
    "le": lambda a, b: int(a) <= int(b),
}


class Runner:
    def __init__(
        self,
        core: NooCore,
        base: Path,
        name: str,
        steps: list[Step],
        variables: dict[str, dict[str, str | int]],
        allow_shell: bool = False,
    ) -> None:
        self.core = core
        self.base = base
        self.name = name
        self.steps = steps
        self.vars = variables
        self.shell = allow_shell

    def _resolve_var(self, var: str) -> str | int:
        if var.startswith("$$"):
            var = var[2:]

        ns, name = var.split(":", 1)

        if ns not in ("noo", "var"):
            raise RunnerError(f"Unknown variable namespace: {ns} (during string formatting, noofile: {self.name})")

        if name not in self.vars[ns]:
            raise RunnerError(f"Unknown variable: {ns}:{name} (during string formatting, noofile: {self.name})")

        return self.vars[ns][name]

    def _run_replace(self, files: list[str], src: str, dest: str) -> None:
        for file in files:
            path = self.base / file

            if not path.exists():
                raise RunnerError(f"No such file: {path} (in replace action, noofile: {self.name})")

            source = path.read_text()
            target = replace(source, src, dest, self.vars)
            path.write_text(target)

    def _run_delete(self, files: list[str]) -> None:
        for file in files:
            path = self.base / file

            if path.exists():
                path.unlink()

    def _run_create(self, file: str, content: str) -> None:
        path = self.base / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(format_vars(content, self.vars))

    def _run_rename(self, file: str, dest: str) -> None:
        path = self.base / file

        if not path.exists():
            raise RunnerError(f"No such file: {path} (in rename action, noofile {self.name})")

        path.rename(self.base / dest)

    def _verify_step_conditions(self, step: Step) -> bool:
        if step.conditions is None:
            return True

        for condition in step.conditions:
            var = self._resolve_var(condition.var)
            value = condition.value

            op = OPMAP[condition.op]

            if not op(var, value):
                return False

        return True

    def _run_command(self, command: str, fail: bool, cwd: str | Path) -> None:
        if not self.shell:
            if fail:
                raise RunnerError(
                    f"Command `{command}` is required but shell commands are not allowed. If you wish to run this command please use --shell."
                )

            echo(
                f"Skipping command as shell is disabled. If you wish to run this command please use --shell.\n  Command: {command}"
            )
            return

        _cwd = Path(format_vars(cwd, self.vars) if isinstance(cwd, str) else cwd)
        proc = Popen(format_vars(command, self.vars), cwd=_cwd, stdout=PIPE, stderr=PIPE, shell=True)

        out, err = proc.communicate()

        if fail and proc.returncode:
            raise RunnerError(f"Command failed: {command}\n{err.decode()}")

        echo(out.decode())

    def _run_step(self, step: Step) -> None:
        if not self._verify_step_conditions(step):
            echo(f"Skipping step {step.name}.")
            return

        for action in step.actions:
            if isinstance(action, ReplaceAction):
                self._run_replace(action.files, action.src, action.dest)
            elif isinstance(action, DeleteAction):
                self._run_delete(action.files)
            elif isinstance(action, CreateAction):
                self._run_create(action.file, action.content or "")
            elif isinstance(action, RenameAction):
                self._run_rename(action.file, action.dest)
            elif isinstance(action, CommandAction):
                self._run_command(action.command, action.fail, action.cwd or self.base)
            elif isinstance(action, RemoteAction):
                self.core.mod(action.remote, self.base, self.vars)
            else:
                raise RunnerError(f"Invalid action: {action} (noofile: {self.name})")

    def run(self) -> None:
        for step in self.steps:
            echo(f"Running step {step.name}.")

            self._run_step(step)
