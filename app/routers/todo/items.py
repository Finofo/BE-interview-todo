from fastapi import APIRouter

router = APIRouter()


@router.get("/todo/items", tags=["users"])
async def get_todo_items():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/todo/items/{id}", tags=["users"])
async def get_todo_item(id: str):
    return {"username": "id"}
