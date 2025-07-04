from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


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

    id: str
    title: str
    description: Optional[str] = None
    is_completed: bool
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)
