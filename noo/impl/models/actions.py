from typing import List, Literal, Optional, Union

from pydantic import BaseModel


class Action(BaseModel):
    action: str


class ReplaceAction(Action):
    action: Literal["replace"]
    files: List[str]
    src: str
    dest: str


class DeleteAction(Action):
    action: Literal["delete"]
    files: List[str]


class CreateAction(Action):
    action: Literal["create"]
    file: str
    content: Optional[str] = None


class RenameAction(Action):
    action: Literal["rename"]
    file: str
    dest: str


class CopyAction(Action):
    action: Literal["copy"]
    file: str
    dest: str


class CommandAction(Action):
    action: Literal["command"]
    command: str
    fail: bool = True
    cwd: Optional[str] = None


class RemoteAction(Action):
    action: Literal["remote"]
    remote: str


class FormatAction(Action):
    action: Literal["format"]
    files: list[str]


class ReadAction(Action):
    action: Literal["read"]
    name: str
    prompt: Optional[str] = None
    default: Optional[str] = None


ActionType = Union[
    ReplaceAction,
    DeleteAction,
    CreateAction,
    RenameAction,
    CopyAction,
    CommandAction,
    RemoteAction,
    FormatAction,
    ReadAction,
    Action,
]
