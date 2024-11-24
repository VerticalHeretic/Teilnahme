from fastapi import APIRouter, HTTPException, status

from src.common.errors import SemesterError
from src.common.models import DegreeName, Student
from src.modules.students_operations import (
    StudentsOperationsDep,
    StudentValidationError,
)

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/")
async def get_students(
    students_operations: StudentsOperationsDep,
    degree: DegreeName | None = None,
    semester: int | None = None,
) -> list[Student]:
    if degree is not None and semester is not None:
        try:
            return students_operations.get_students_in_degree(degree, semester)
        except SemesterError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            ) from e
    elif degree is not None:
        return students_operations.get_students_in_degree(degree)
    return students_operations.get_students()


@router.post("/", response_model=Student)
async def add_student(
    students_operations: StudentsOperationsDep, student: Student
) -> Student:
    try:
        return students_operations.add_student(student)
    except (StudentValidationError, SemesterError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.put("/{student_id}", status_code=status.HTTP_200_OK)
async def update_student(
    students_operations: StudentsOperationsDep, student_id: int, student: Student
) -> Student:
    return students_operations.update_student(student_id, student)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(students_operations: StudentsOperationsDep, student_id: int):
    students_operations.delete_student(student_id)
