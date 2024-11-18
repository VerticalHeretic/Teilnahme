from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class DegreeName(str, Enum):
    master = "Master"
    bachelor = "Bachelor"


class Student(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    surname: str
    degree: DegreeName
    semester: int


class Subject(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    semester: int
    degree: DegreeName


class BaseClassroom(BaseModel):
    students_ids: list[int]
    subject_id: int


class Classroom(BaseClassroom):
    id: int


class BaseAttendenceRecord(BaseModel):
    student_id: int
    classroom_id: int
    date: datetime


class AttendenceRecord(BaseAttendenceRecord):
    id: int
