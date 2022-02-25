from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .actions import ActionType


class ReadVariable(BaseModel):
    name: str
    prompt: Optional[str] = None
    default: Optional[str] = None


class Step(BaseModel):
    name: str
    actions: list[ActionType] = []


class Noofile(BaseModel):
    name: Optional[str] = None
    remote: str
    read: list[ReadVariable] = []
    steps: list[Step] = []
