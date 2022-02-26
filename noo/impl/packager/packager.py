from __future__ import annotations

from pathlib import Path
from typing import Type

from typer import echo
from yaml import safe_dump

from .runners import AutoPackagerRunner, JavaScriptRunner, PythonPoetryRunner

RUNNERS: list[Type[AutoPackagerRunner]] = [
    JavaScriptRunner,
    PythonPoetryRunner,
]


class Packager:
    def __init__(self, location: Path) -> None:
        runner = None

        for runner_type in RUNNERS:
            if runner_type.detect(location):
                runner = runner_type(location)
                echo(f"Using packager {runner.__class__.__name__}")
                break

        if runner is None:
            raise ValueError(f"No packager found for {location}")

        self.runner = runner

    def package(self, to: Path) -> None:
        spec = self.runner.package()

        to.write_text(safe_dump(spec.dict()))
