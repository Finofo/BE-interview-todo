from fastapi import FastAPI

from .routers import todo_items

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(todo_items)
