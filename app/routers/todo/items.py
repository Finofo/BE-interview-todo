from fastapi import APIRouter, Depends, HTTPException
import uuid

from app.logic import todo_item_logic
from app.database import get_session
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/todo/items", tags=["todo"])
async def list_todo_items(session: Session = Depends(get_session)):
    todo_items = todo_item_logic.list_todo_items(session)

    return todo_items


@router.get("/todo/items/{id}", tags=["todo"])
async def get_todo_item(id: str, session: Session = Depends(get_session)):
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    todo_item = todo_item_logic.get_todo_item_by_id(session, todo_id)
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")

    return todo_item
