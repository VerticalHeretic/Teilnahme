from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class DegreeName(str, Enum):
    master = "Master"
    bachelor = "Bachelor"

class BaseStudent(BaseModel):
    name: str
    surname: str
    degree: DegreeName
    semester: int

class Student(BaseStudent):
    id: int

class BaseSubject(BaseModel):
    name: str
    semester: int
    degree: DegreeName

class Subject(BaseSubject):
    id: int

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
