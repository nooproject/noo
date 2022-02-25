from __future__ import annotations

from pathlib import Path

from typer import echo

from .formatter import replace
from ..models import Step, ReplaceAction


class Runner:
    def __init__(self, base: Path, steps: list[Step], variables: dict[str, dict[str, str | int]]) -> None:
        self.base = base
        self.steps = steps
        self.vars = variables

    def _run_replace(self, files: list[str], src: str, dest: str) -> None:
        for file in files:
            path = self.base / file

            source = path.read_text()
            target = replace(source, src, dest, self.vars)
            path.write_text(target)

    def _run_step(self, step: Step) -> None:
        for action in step.actions:
            if isinstance(action, ReplaceAction):
                self._run_replace(action.files, action.src, action.dest)

    def run(self) -> None:
        for step in self.steps:
            echo(f"Running step {step.name}.")

            self._run_step(step)
