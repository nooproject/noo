from json import dumps, loads
from pathlib import Path


def save(name: str, ref: str) -> None:
    nooconf = Path.home() / ".config" / "noo"
    nooconf.mkdir(parents=True, exist_ok=True)

    registry = nooconf / "registry.json"

    refl = Path(ref).absolute()

    if not registry.exists():
        registry.touch()
        registry.write_text(dumps({name: str(refl)}))

        return

    data = loads(registry.read_text())
    data[name] = str(refl)

    registry.write_text(dumps(data))


def load() -> dict[str, str]:
    nooconf = Path.home() / ".config" / "noo"
    nooconf.mkdir(parents=True, exist_ok=True)

    registry = nooconf / "registry.json"

    if not registry.exists():
        return {}

    return loads(registry.read_text())
