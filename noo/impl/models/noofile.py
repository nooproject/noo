from typing import Optional

from pydantic import BaseModel

from .actions import ActionType, List


class ReadVariable(BaseModel):
    name: str
    prompt: Optional[str] = None
    default: Optional[str] = None


class Step(BaseModel):
    name: str
    actions: List[ActionType] = []


class Noofile(BaseModel):
    name: Optional[str] = None
    remote: str
    read: List[ReadVariable] = []
    steps: List[Step] = []
