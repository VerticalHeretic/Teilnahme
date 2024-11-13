import pytest

from typing import Dict, Any, List
from src.modules.students_operations import StorageHandler, StudentsOperations, StudentDataError
from src.common.models import Student, DegreeName, BaseStudent


class MockStudentsStorage(StorageHandler):
    def __init__(self, students: List[Student]):
        self.students = students
    
    def save(self, data: Dict[str, Any]):
        self.students.append(data)

    def load(self) -> List[Dict[str, Any]]:
        return [s.model_dump() for s in self.students]

    def delete(self, id: int):
        self.students = [s for s in self.students if s.id != id]
        
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

    def test_get_students_raises_error_when_invalid_student_data(self):
        # Given
        student = BaseStudent(name="John", surname="Daw", degree=DegreeName.bachelor, semester=4)
        students_storage = MockStudentsStorage([student])
        students_operations = StudentsOperations(students_storage)

        # When
        with pytest.raises(StudentDataError):
            students_operations.get_students()

            # Then
            assert True


