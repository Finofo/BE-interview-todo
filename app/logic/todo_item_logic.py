from typing_extensions import Optional
import uuid
from sqlalchemy.orm import Session

from app.models.todo_item import TodoItem


def get_todo_item_by_id(session: Session, todo_id: uuid.UUID) -> Optional[TodoItem]:
    """
    Fetch a TodoItem from the database by its UUID.

    Args:
        session: SQLAlchemy database session
        todo_id: UUID of the todo item to fetch

    Returns:
        TodoItem object if found, None otherwise
    """
    query = session.query(TodoItem).filter(TodoItem.id == todo_id)

    return query.first()


def list_todo_items(
    session: Session, completed: Optional[bool] = None
) -> list[TodoItem]:
    """
    Retrieve a list of TodoItems from the database with optional.

    Args:
        session: SQLAlchemy database session
        completed: If provided, filter by completion status

    Returns:
        List of TodoItem objects
    """
    query = session.query(TodoItem)

    if completed is not None:
        query = query.filter(TodoItem.is_completed == completed)

    return query.order_by(TodoItem.created_at.desc()).all()
