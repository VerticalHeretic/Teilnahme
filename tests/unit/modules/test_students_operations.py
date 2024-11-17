import pytest

from typing import Dict, Any, List
from src.modules.students_operations import StudentsOperations, StudentDataError
from src.common.models import Student, DegreeName, BaseStudent
from src.common.storage.storage import StorageHandler

class MockStudentsStorage(StorageHandler):
    def __init__(self, students: List[Student]):
        self.students = students
    
    def save(self, data: Dict[str, Any]):
        self.students.append(Student(**data))

    def load(self) -> List[Dict[str, Any]]:
        return [s.model_dump() for s in self.students]

    def delete(self, id: int):
        self.students = [s for s in self.students if s.id != id]
    
    def update(self, id: int, data: Dict[str, Any]):
        index = next((index for index, student in enumerate(self.students) if student.id == id), None)
        
        if index is not None:
            self.students[index] = Student(**data)

    def generate_id(self) -> int:
        return len(self.students) + 1

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
        student = BaseStudent(name="John", surname="Daw", degree=DegreeName.bachelor, semester=4)
        students_storage = MockStudentsStorage([])
        students_operations = StudentsOperations(students_storage)
        want = [Student(id=1, **student.model_dump())]

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

        updated_student = BaseStudent(name="Jane", surname="Smith", degree=DegreeName.bachelor, semester=6)

        # When
        students_operations.update_student(student.id, updated_student)

        # Then
        assert students_storage.students == [Student(id=1, **updated_student.model_dump())]
