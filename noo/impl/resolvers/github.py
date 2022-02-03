from pathlib import Path
from re import compile
from tempfile import gettempdir
from zipfile import ZipFile
from shutil import move

from requests import get

REPO = compile(
    r"(?P<author>[a-zA-Z0-9_-]+)\/(?P<repo>[a-zA-Z0-9_-]+)(@(?P<branch>[a-zA-Z0-9_-]+))?"
)


def clone_github(repo: str, dest: Path) -> None:
    match = REPO.search(repo)

    if not match:
        raise ValueError(f"Invalid repo: {repo}")

    url = (
        f"https://github.com/{match.group('author')}/{match.group('repo')}"
        f"/archive/refs/heads/{match.group('branch') or 'master'}.zip"
    )

    temp_path = Path(gettempdir()) / f"{hash(url)}.zip"
    temp_path.write_bytes(get(url).content)

    with ZipFile(temp_path) as zip_file:
        print("Cloned to ", dest.absolute())
        zip_file.extractall(dest.parent)

    move(dest.parent / f"{match.group('repo')}-{match.group('branch') or 'master'}", dest)
