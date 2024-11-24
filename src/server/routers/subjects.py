from fastapi import APIRouter, HTTPException, status

from src.common.errors import NotFoundError, SemesterError
from src.common.models import DegreeName, Subject
from src.modules.subjects_operations import (
    SubjectsOperationsDep,
    SubjectValidationError,
)

subjects_router = APIRouter(prefix="/subjects", tags=["subjects"])
subject_router = APIRouter(prefix="/subject", tags=["subject"])


@subjects_router.get("/")
async def get_subjects(
    subjects_operations: SubjectsOperationsDep,
    degree: DegreeName | None = None,
    semester: int | None = None,
) -> list[Subject]:
    if degree is not None and semester is not None:
        try:
            return subjects_operations.get_subjects_in_degree(degree, semester)
        except SemesterError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            ) from e
    elif degree is not None:
        return subjects_operations.get_subjects_in_degree(degree)
    return subjects_operations.get_subjects()


@subject_router.get("/{subject_id}")
async def get_subject(
    subjects_operations: SubjectsOperationsDep, subject_id: int
) -> Subject:
    try:
        return subjects_operations.get_subject(subject_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@subjects_router.post("/", response_model=Subject)
async def add_subject(
    subjects_operations: SubjectsOperationsDep, subject: Subject
) -> Subject:
    try:
        return subjects_operations.add_subject(subject)
    except (SubjectValidationError, SemesterError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@subjects_router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(subjects_operations: SubjectsOperationsDep, subject_id: int):
    try:
        subjects_operations.delete_subject(subject_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@subjects_router.put("/{subject_id}", status_code=status.HTTP_200_OK)
async def update_subject(
    subjects_operations: SubjectsOperationsDep, subject_id: int, subject: Subject
):
    try:
        return subjects_operations.update_subject(subject_id, subject)
    except (SubjectValidationError, SemesterError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
