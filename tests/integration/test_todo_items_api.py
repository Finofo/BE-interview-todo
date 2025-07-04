import uuid
from datetime import datetime

from app.models.todo_item import TodoItem


def test_create_and_get_todo_item(client):
    """Test creating a todo item via POST and retrieving it via GET."""
    # Create a new todo item
    response = client.post(
        "/todo/items",
        json={
            "title": "Test todo",
            "description": "This is a test",
            "is_completed": False,
        },
    )

    # Verify POST response
    assert response.status_code == 201
    created_item = response.json()
    assert created_item["title"] == "Test todo"
    assert created_item["description"] == "This is a test"
    assert created_item["is_completed"] is False

    # Verify that the UUID is valid
    item_id = created_item["id"]
    uuid.UUID(item_id)  # This will raise an exception if the ID is not a valid UUID

    # Verify timestamps are ISO 8601 format
    created_at = datetime.fromisoformat(
        created_item["created_at"].replace("Z", "+00:00")
    )
    updated_at = datetime.fromisoformat(
        created_item["updated_at"].replace("Z", "+00:00")
    )
    assert isinstance(created_at, datetime)
    assert isinstance(updated_at, datetime)

    # Get the created todo item by ID
    response = client.get(f"/todo/items/{item_id}")

    # Verify GET response
    assert response.status_code == 200
    retrieved_item = response.json()
    assert retrieved_item["id"] == item_id
    assert retrieved_item["title"] == "Test todo"
    assert retrieved_item["description"] == "This is a test"
    assert retrieved_item["is_completed"] is False


def test_list_todo_items(client, db_session):
    """Test listing all todo items."""
    # Create a few todo items directly in the database
    items = [
        TodoItem(
            title=f"Todo {i}",
            description=f"Description {i}" if i % 2 == 0 else None,
            is_completed=i % 2 == 0,
        )
        for i in range(3)
    ]

    for item in items:
        db_session.add(item)
    db_session.commit()

    # Get all todo items
    response = client.get("/todo/items")

    # Verify response
    assert response.status_code == 200
    retrieved_items = response.json()

    # Verify we got all 3 items
    assert len(retrieved_items) == 3

    # Verify items are returned in reverse chronological order (newest first)
    for i, item in enumerate(retrieved_items):
        # Items should be in reverse order from how we created them
        expected_idx = 2 - i
        assert item["title"] == f"Todo {expected_idx}"

        if expected_idx % 2 == 0:
            assert item["description"] == f"Description {expected_idx}"
            assert item["is_completed"] is True
        else:
            assert item["description"] is None
            assert item["is_completed"] is False


def test_get_nonexistent_todo_item(client):
    """Test getting a todo item that doesn't exist."""
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/todo/items/{non_existent_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo item not found"}


def test_get_todo_item_invalid_id(client):
    """Test getting a todo item with an invalid UUID."""
    response = client.get("/todo/items/not-a-uuid")

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid UUID format"}


def test_create_todo_item_validation(client):
    """Test validation when creating a todo item with invalid data."""
    # Test with missing required field
    response = client.post(
        "/todo/items",
        json={"description": "Missing title field"},
    )
    assert response.status_code == 422

    # Test with empty title
    response = client.post(
        "/todo/items",
        json={"title": "", "description": "Empty title"},
    )
    assert response.status_code == 422

    # Test with title too long (>255 chars)
    response = client.post(
        "/todo/items",
        json={"title": "x" * 256, "description": "Title too long"},
    )
    assert response.status_code == 422
