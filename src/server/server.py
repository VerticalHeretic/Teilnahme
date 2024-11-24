from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.common.storage.db_storage import create_db_and_tables
from src.server.routers import classrooms, students, subjects


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Students
app.include_router(students.router)

# Subjects
app.include_router(subjects.subjects_router)
app.include_router(subjects.subject_router)

# Classrooms
app.include_router(classrooms.classrooms_router)
app.include_router(classrooms.classroom_router)

# Attendance


@app.get("/")
async def root():
    return {"message": "Hello World!"}
