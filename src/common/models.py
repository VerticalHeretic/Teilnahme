from datetime import datetime
from enum import Enum
from typing import List

from sqlmodel import Field, Relationship, SQLModel


class DegreeName(str, Enum):
    master = "Master"
    bachelor = "Bachelor"


class StudentClassroomLink(SQLModel, table=True):
    student_id: int = Field(default=None, foreign_key="student.id", primary_key=True)
    classroom_id: int = Field(
        default=None, foreign_key="classroom.id", primary_key=True
    )


class Student(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    surname: str
    degree: DegreeName
    semester: int
    classrooms: List["Classroom"] = Relationship(
        back_populates="students", link_model=StudentClassroomLink
    )

    def __str__(self) -> str:
        return f"{self.name} {self.surname} - {self.degree.value} (Semester {self.semester})"


class Classroom(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    subject_id: int
    students: List[Student] = Relationship(
        back_populates="classrooms", link_model=StudentClassroomLink
    )

    def __str__(self) -> str:
        return f"Classroom for subject with id: {self.subject_id} with {len(self.students)} students"


class Subject(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    semester: int
    degree: DegreeName

    def __str__(self) -> str:
        return f"{self.name} - for: {self.degree.value} degree at semester: {self.semester}"


class AttendenceRecord(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    student_id: int
    classroom_id: int
    date: datetime

    def __str__(self) -> str:
        return f"Attendance: {self.student_id} in classroom: {self.classroom_id} on {self.date}"
