from typing import Literal, Union, List

from pydantic import BaseModel


class Action(BaseModel):
    action: str


class ReplaceAction(Action):
    action: Literal["replace"]
    files: List[str]
    src: str
    dest: str


ActionType = Union[ReplaceAction, Action]
