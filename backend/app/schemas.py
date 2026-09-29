from typing import Optional

from pydantic import BaseModel


class ExtractRequest(BaseModel):
    notes: str


class ExtractedTask(BaseModel):
    title: str
    assignee: Optional[str] = None
    due_date: Optional[str] = None


class ExtractResponse(BaseModel):
    tasks: list[ExtractedTask]