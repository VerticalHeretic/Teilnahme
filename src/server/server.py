from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from enum import Enum
from fastapi.exceptions import HTTPException
from sqlmodel import select
from src.common.models import Student, DegreeName, BaseStudent
from src.common.storage.db_storage import SessionDep, create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/students/")
async def get_students(session: SessionDep) -> list[Student]:
    return session.exec(select(Student)).all()

@app.get("/students/{degree_name}")
async def get_students_in_degree(session: SessionDep, degree_name: DegreeName, semester: int | None = None) -> list[Student]:
    if degree_name is DegreeName.bachelor and isinstance(semester,int) and semester > 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bachelor degree has only 6 semesters")
    elif degree_name is DegreeName.master and isinstance(semester,int) and semester > 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Master degree has only 4 semesters")
    
    return session.exec(select(Student)
                            .where(Student.degree == degree_name)
                            .where(Student.semester == semester if semester is not None else True)).all()

@app.post("/students/")
async def add_student(session: SessionDep, student: Student) -> Student:
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.put("/students/{student_id}", status_code=status.HTTP_200_OK)
async def update_student(session: SessionDep, student_id: int, student: Student) -> Student:
    student_db = session.get(Student, student_id)
    if not student_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    student_data = student.model_dump(exclude_unset=True)
    student_db.sqlmodel_update(student_data)
    session.add(student_db)
    session.commit()
    session.refresh(student_db)    

    return student_db

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(session: SessionDep, student_id: int):
    student_db = session.get(Student, student_id)
    if not student_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    session.delete(student_db)
    session.commit()
