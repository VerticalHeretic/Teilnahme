from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from enum import Enum
from fastapi.exceptions import HTTPException
from sqlmodel import select
from src.common.models import Student, DegreeName
from src.common.storage.db_storage import SessionDep, create_db_and_tables
from src.modules.students_operations import StudentsOperationsDep 

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/students/")
async def get_students(students_operations: StudentsOperationsDep) -> list[Student]:
    return students_operations.get_students()

@app.get("/students/{degree_name}")
async def get_students_in_degree(session: SessionDep, degree_name: DegreeName, semester: int | None = None) -> list[Student]:
    if degree_name is DegreeName.bachelor and isinstance(semester,int) and semester > 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bachelor degree has only 6 semesters")
    elif degree_name is DegreeName.master and isinstance(semester,int) and semester > 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Master degree has only 4 semesters")
    
    return list(session.exec(select(Student)
                            .where(Student.degree == degree_name)
                            .where(Student.semester == semester if semester is not None else True)).all())

@app.post("/students/")
async def add_student(students_operations: StudentsOperationsDep, student: Student) -> Student:
    return students_operations.add_student(student)

@app.put("/students/{student_id}", status_code=status.HTTP_200_OK)
async def update_student(students_operations: StudentsOperationsDep, student_id: int, student: Student) -> Student:
    return students_operations.update_student(student_id, student)

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(students_operations: StudentsOperationsDep, student_id: int):
    students_operations.delete_student(student_id)
