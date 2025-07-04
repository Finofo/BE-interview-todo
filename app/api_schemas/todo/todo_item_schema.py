from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_serializer


class TodoItemCreate(BaseModel):
    """
    Schema for creating a new todo item.
    """

    title: str = Field(
        ..., min_length=1, max_length=255, description="The title of the todo item"
    )
    description: Optional[str] = Field(
        None, description="An optional description of the todo item"
    )
    is_completed: bool = Field(False, description="Whether the todo item is completed")


class TodoItemResponse(BaseModel):
    """
    Schema for todo item responses.
    """

    id: UUID
    title: str
    description: Optional[str] = None
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.isoformat()
