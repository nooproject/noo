from typing import Literal, Optional

from pydantic import BaseModel, Field

from .actions import ActionType, List


class ReadVariable(BaseModel):
    name: str
    prompt: Optional[str] = None
    default: Optional[str] = None
    required: bool = True


class Condition(BaseModel):
    op: Literal["eq", "ne", "gt", "ge", "lt", "le"]
    var: str
    value: str


class Step(BaseModel):
    name: str
    actions: List[ActionType] = Field(default_factory=list)
    conditions: Optional[List[Condition]] = None


class BaseNoofile(BaseModel):
    noo_version: Literal[2]
    name: str
    read: List[ReadVariable] = Field(default_factory=list)
    steps: List[Step] = Field(default_factory=list)
    version: Optional[str] = None


class Noofile(BaseNoofile):
    remote: str
