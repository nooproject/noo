from json import loads
from pathlib import Path

from ...models import Noofile, ReadVariable, ReplaceAction, Step


class JavaScriptRunner:
    def __init__(self, location: Path) -> None:
        self.location = location

    def package(self, remote: str) -> Noofile:
        package = self.location / "package.json"
        package_data = loads(package.read_text())

        name = package_data["name"]
        author = package_data["author"]
        desc = package_data["description"]

        noofile = Noofile(
            name=name.title(),
            remote=remote,
            noo_version=2,
        )

        package_json_step = Step(name="Update package.json")

        actions = [
            ReplaceAction(
                action="replace",
                files=["package.json"],
                src=f'"name": "{name}"',
                dest=f'"name": "$$noo:name"',
            ),
            ReplaceAction(
                action="replace",
                files=["package.json"],
                src=author,
                dest=f"$$var:author <$$var:email>",
            ),
            ReplaceAction(
                action="replace",
                files=["package.json"],
                src=f'"{desc}"',
                dest=f'"$$var:description"',
            ),
        ]

        package_json_step.actions.extend(actions)
        noofile.steps.append(package_json_step)

        noofile.read = [
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
        path = location / "package.json"

        return path.exists()
