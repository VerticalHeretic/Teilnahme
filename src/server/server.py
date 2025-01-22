from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.common.storage.db_storage import create_db_and_tables
from src.server.routers import students


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Include the students router
app.include_router(students.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
