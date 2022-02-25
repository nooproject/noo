from __future__ import annotations

from pathlib import Path

from typer import echo

from ..models import CreateAction, DeleteAction, RenameAction, ReplaceAction, Step
from .formatter import replace, format_vars


class Runner:
    def __init__(
        self, base: Path, steps: list[Step], variables: dict[str, dict[str, str | int]]
    ) -> None:
        self.base = base
        self.steps = steps
        self.vars = variables

    def _run_replace(self, files: list[str], src: str, dest: str) -> None:
        for file in files:
            path = self.base / file

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
        path.write_text(format_vars(content, self.vars))

    def _run_rename(self, file: str, dest: str) -> None:
        path = self.base / file

        if not path.exists():
            raise ValueError(f"No such file: {path}")

        path.rename(self.base / dest)

    def _run_step(self, step: Step) -> None:
        for action in step.actions:
            if isinstance(action, ReplaceAction):
                self._run_replace(action.files, action.src, action.dest)
            elif isinstance(action, DeleteAction):
                self._run_delete(action.files)
            elif isinstance(action, CreateAction):
                self._run_create(action.file, action.content or "")
            elif isinstance(action, RenameAction):
                self._run_rename(action.file, action.dest)
            else:
                raise ValueError(f"Invalid action: {action}")

    def run(self) -> None:
        for step in self.steps:
            echo(f"Running step {step.name}.")

            self._run_step(step)
