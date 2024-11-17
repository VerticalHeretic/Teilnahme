import pytest

from typing import Dict, Any, List, Type
from src.modules.students_operations import StudentsOperations
from src.common.models import Student, DegreeName
from src.common.storage.storage import NewStorageHandler
from sqlmodel import SQLModel
    
class MockStudentsStorage(NewStorageHandler):
    def __init__(self, students: List[Student]):
        self.students = students
    
    def get_all(self, model_type: Type[SQLModel]) -> List[SQLModel]:
        return [s for s in self.students if isinstance(s, model_type)]

    def get_by_id(self, id: int, model_type: Type[SQLModel]) -> SQLModel:
        return next((s for s in self.students if isinstance(s, model_type) and s.id == id), None)
    
    def create(self, model: SQLModel):
        student = Student(id=len(self.students) + 1, **model.model_dump(exclude_unset=True))
        self.students.append(student)

    def update(self, id: int, model: SQLModel):
        index = next((index for index, student in enumerate(self.students) if student.id == id), None)
        
        if index is not None:
            self.students[index] = model

    def delete(self, id: int, model_type: Type[SQLModel]):
        self.students = [s for s in self.students if isinstance(s, model_type) and s.id != id]

class TestStudentsOperations:

    def test_get_students(self):
        # Given
        student = Student(id=1, name="John", surname="Daw", degree=DegreeName.bachelor, semester=4)
        students_storage = MockStudentsStorage([student])
        students_operations = StudentsOperations(students_storage)
        want = [student]

        # When 
        got = students_operations.get_students()

        # Then
        assert got == want

    def test_get_empty_list_when_no_students(self):
        # Given
        students_storage = MockStudentsStorage([])
        students_operations = StudentsOperations(students_storage)
        want = []

        # When
        got = students_operations.get_students()

        # Then
        assert got == want

    def test_add_student(self):
        # Given
        student = Student(name="John", surname="Daw", degree=DegreeName.bachelor, semester=4)
        students_storage = MockStudentsStorage([])
        students_operations = StudentsOperations(students_storage)
        want = [Student(id=1, **student.model_dump(exclude_unset=True))]

        # When 
        students_operations.add_student(student)

        # Then
        assert students_storage.students == want

    def test_delete_student(self):
        # Given
        student = Student(id=1, name="John", surname="Daw", degree=DegreeName.bachelor, semester=4)
        students_storage = MockStudentsStorage([student])
        students_operations = StudentsOperations(students_storage)

        # When
        students_operations.delete_student(student.id)

        # Then
        assert students_storage.students == []

    def test_update_student(self):
        # Given
        student = Student(id=1, name="John", surname="Daw", degree=DegreeName.bachelor, semester=4)
        students_storage = MockStudentsStorage([student])
        students_operations = StudentsOperations(students_storage)

        updated_student = Student(id=1, name="Jane", surname="Smith", degree=DegreeName.bachelor, semester=6)

        # When
        students_operations.update_student(student.id, updated_student)

        # Then
        assert students_storage.students == [updated_student]
