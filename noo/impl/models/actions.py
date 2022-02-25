from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel


class Action(BaseModel):
    action: str


class ReplaceAction(Action):
    action: Literal["replace"]
    files: list[str]
    src: str
    dest: str


ActionType = Union[ReplaceAction, Action]
