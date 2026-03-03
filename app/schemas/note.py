from pydantic import BaseModel, Field
from datetime import datetime


class NoteCreate(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    user_note_number: int
    created_at: datetime

    model_config = {"from_attributes": True}
