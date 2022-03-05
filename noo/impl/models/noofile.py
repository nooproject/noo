from typing import Literal, Optional

from pydantic import BaseModel

from .actions import ActionType, List


class ReadVariable(BaseModel):
    name: str
    prompt: Optional[str] = None
    default: Optional[str] = None


class Condition(BaseModel):
    op: Literal["eq", "ne", "gt", "ge", "lt", "le"]
    var: str
    value: str


class Step(BaseModel):
    name: str
    actions: List[ActionType] = []
    conditions: Optional[List[Condition]] = None


class BaseNoofile(BaseModel):
    noo_version: int
    name: str
    read: List[ReadVariable] = []
    steps: List[Step] = []


class Noofile(BaseNoofile):
    remote: str
