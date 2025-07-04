from typing_extensions import Optional
import uuid
from sqlalchemy.orm import Session

from app.api_schemas.todo import TodoItemCreate
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


def list_todo_items(session: Session) -> list[TodoItem]:
    """
    Retrieve a list of TodoItems from the database with optional.

    Args:
        session: SQLAlchemy database session

    Returns:
        List of TodoItem objects
    """
    query = session.query(TodoItem)

    return query.order_by(TodoItem.created_at.desc()).all()


def create_todo_item(session: Session, todo_item_create: TodoItemCreate) -> TodoItem:
    """
    Create a new TodoItem in the database.

    Args:
        session: SQLAlchemy database session
        todo_create: Data for creating the new todo item

    Returns:
        The created TodoItem object
    """
    # Create a new TodoItem instance
    todo_item = TodoItem(
        title=todo_item_create.title,
        description=todo_item_create.description,
        is_completed=todo_item_create.is_completed,
    )

    # Add to session and commit to generate ID and timestamps
    session.add(todo_item)
    session.commit()
    session.refresh(todo_item)

    return todo_item
