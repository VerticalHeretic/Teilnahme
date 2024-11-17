from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from src.common.models import Student, DegreeName
from src.common.storage.db_storage import create_db_and_tables
from src.modules.students_operations import StudentsOperationsDep, StudentBachelorSemesterError, StudentMasterSemesterError

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
async def get_students_in_degree(students_operations: StudentsOperationsDep, degree_name: DegreeName, semester: int | None = None) -> list[Student]:
    try:
        return students_operations.get_students_in_degree(degree_name, semester)
    except StudentBachelorSemesterError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except StudentMasterSemesterError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

@app.post("/students/")
async def add_student(students_operations: StudentsOperationsDep, student: Student) -> Student:
    return students_operations.add_student(student)

@app.put("/students/{student_id}", status_code=status.HTTP_200_OK)
async def update_student(students_operations: StudentsOperationsDep, student_id: int, student: Student) -> Student:
    return students_operations.update_student(student_id, student)

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(students_operations: StudentsOperationsDep, student_id: int):
    students_operations.delete_student(student_id)
