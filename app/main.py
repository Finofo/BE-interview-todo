from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import Base, engine
from .models import *  # noqa
from .routers import todo_items


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Add cleanup code here if needed
    pass


app = FastAPI(lifespan=lifespan)

app.include_router(todo_items)
