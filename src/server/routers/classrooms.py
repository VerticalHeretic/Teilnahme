from fastapi import APIRouter, HTTPException

from src.common.errors import NotFoundError
from src.common.models import Classroom
from src.modules.classrooms_operations import ClassroomsOperationsDep

classrooms_router = APIRouter(prefix="/classrooms", tags=["classrooms"])
classroom_router = APIRouter(prefix="/classroom", tags=["classroom"])


@classrooms_router.get("/")
async def get_classrooms(
    classrooms_operations: ClassroomsOperationsDep,
    subject_id: int | None = None,
    student_id: int | None = None,
):
    if subject_id is not None:
        return classrooms_operations.get_classrooms_where_subject(subject_id)
    if student_id is not None:
        return classrooms_operations.get_classrooms_where_student(student_id)
    return classrooms_operations.get_classrooms()


@classroom_router.get("/{classroom_id}")
async def get_classroom(
    classrooms_operations: ClassroomsOperationsDep, classroom_id: int
):
    try:
        return classrooms_operations.get_classroom(classroom_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@classroom_router.post("/")
async def create_classroom(
    classrooms_operations: ClassroomsOperationsDep, classroom: Classroom
):
    return classrooms_operations.create_classroom(classroom)


@classroom_router.delete("/{classroom_id}")
async def delete_classroom(
    classrooms_operations: ClassroomsOperationsDep, classroom_id: int
):
    classrooms_operations.delete_classroom(classroom_id)


@classroom_router.post("/{classroom_id}/students/{student_id}")
async def add_student_to_classroom(
    classrooms_operations: ClassroomsOperationsDep, classroom_id: int, student_id: int
):
    try:
        return classrooms_operations.add_student_to_classroom(classroom_id, student_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@classroom_router.delete("/{classroom_id}/students/{student_id}")
async def remove_student_from_classroom(
    classrooms_operations: ClassroomsOperationsDep, classroom_id: int, student_id: int
):
    try:
        classrooms_operations.delete_student_from_classroom(classroom_id, student_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@classroom_router.put("/{classroom_id}")
async def update_classroom(
    classrooms_operations: ClassroomsOperationsDep,
    classroom_id: int,
    classroom: Classroom,
):
    try:
        return classrooms_operations.update_classroom(classroom_id, classroom)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
