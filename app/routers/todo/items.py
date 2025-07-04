from fastapi import APIRouter, Depends, HTTPException, status
import uuid

from app.logic import todo_item_logic
from app.database import get_session
from sqlalchemy.orm import Session
from app.api_schemas.todo import TodoItemCreate, TodoItemResponse

router = APIRouter()


@router.get("/todo/items", tags=["todo"], response_model=list[TodoItemResponse])
async def list_todo_items(session: Session = Depends(get_session)):
    """
    Retrieve a list of all todo items.

    Parameters:
    - **session**: Database session (injected automatically)

    Returns:
    - List of todo items with their details including title, description,
      completion status, and timestamps
    """
    return todo_item_logic.list_todo_items(session)


@router.post(
    "/todo/items",
    tags=["todo"],
    status_code=status.HTTP_201_CREATED,
    response_model=TodoItemResponse,
)
async def create_todo_item(
    todo_item: TodoItemCreate, session: Session = Depends(get_session)
):
    """
    Create a new todo item.

    Args:
        todo_item: The todo item data
        session: Database session

    Returns:
        The created todo item
    """
    return todo_item_logic.create_todo_item(session, todo_item)


@router.get(
    "/todo/items/{id}",
    tags=["todo"],
    response_model=TodoItemResponse,
)
async def get_todo_item(id: str, session: Session = Depends(get_session)):
    """
    Retrieve a specific todo item by its unique identifier.

    Parameters:
    - **id**: UUID string of the todo item to retrieve

    Returns:
    - Todo item details including title, description, completion status, and timestamps

    Raises:
    - **400 Bad Request**: If the provided ID is not a valid UUID format
    - **404 Not Found**: If no todo item exists with the specified ID
    """
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    todo_item = todo_item_logic.get_todo_item_by_id(session, todo_id)
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")

    return todo_item
