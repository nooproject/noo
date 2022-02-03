from typing import Literal, Optional

from pydantic import BaseModel


class Read(BaseModel):
    name: str
    prompt: Optional[str] = None
    default: Optional[str] = None


class ReplaceAction(BaseModel):
    action: Literal["replace"]
    files: list[str]
    src: str
    dest: str


class Step(BaseModel):
    name: str
    actions: list[ReplaceAction]


class Noofile(BaseModel):
    name: str
    remote: str
    read: list[Read]
    steps: list[Step]
