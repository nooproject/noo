from pathlib import Path

from tomli import loads

from ...models import Noofile, ReadVariable, ReplaceAction, Step


class PythonPoetryRunner:
    def __init__(self, location: Path) -> None:
        self.location = location

    def package(self, remote: str) -> Noofile:
        pyproject = self.location / "pyproject.toml"
        pyproject_data = loads(pyproject.read_text())

        poetry_data = pyproject_data["tool"]["poetry"]

        name = poetry_data["name"]
        author = poetry_data["authors"][0]
        desc = poetry_data["description"]
        repo = poetry_data["repository"]

        noofile = Noofile(
            name=name.title(),
            remote=remote,
            noo_version=2,
        )

        poetry_step = Step(name="Update Poetry")

        actions = [
            ReplaceAction(
                action="replace",
                files=["pyproject.toml"],
                src=f'"name" = "{name}"',
                dest=f'"name" = "$$noo:name"',
            ),
            ReplaceAction(
                action="replace",
                files=["pyproject.toml"],
                src=repo,
                dest=f"$$var:repository",
            ),
            ReplaceAction(
                action="replace",
                files=["pyproject.toml"],
                src=author,
                dest=f"$$var:author <$$var:email>",
            ),
            ReplaceAction(
                action="replace",
                files=["pyproject.toml"],
                src=f'"{desc}"',
                dest=f'"$$var:description"',
            ),
        ]

        poetry_step.actions.extend(actions)
        noofile.steps.append(poetry_step)

        noofile.read = [
            ReadVariable(
                name="repository",
                prompt="Enter repository URL",
            ),
            ReadVariable(
                name="author",
                prompt="Enter author name",
            ),
            ReadVariable(
                name="description",
                prompt="Enter description",
            ),
            ReadVariable(
                name="email",
                prompt="Enter email",
            ),
        ]

        return noofile

    @staticmethod
    def detect(location: Path) -> bool:
        path = location / "pyproject.toml"

        if not path.exists():
            return False

        content = path.read_text()

        return "[tool.poetry]" in content
