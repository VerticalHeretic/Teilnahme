import pytest
from src.modules.classrooms_operations import ClassroomsOperations
from src.common.storage.storage import StorageHandler
from src.common.models import Classroom, BaseClassroom
from typing import List, Dict, Any

class MockClassroomStorage(StorageHandler):
    def __init__(self, classrooms: List[Classroom]):
        self.classrooms = classrooms

    def save(self, data: Dict[str, Any]):
        self.classrooms.append(Classroom(**data))

    def load(self) -> List[Dict[str, Any]]:
        return [c.model_dump() for c in self.classrooms]

    def delete(self, id: int):
        self.classrooms = [c for c in self.classrooms if c.id != id]

    def update(self, id: int, data: Dict[str, Any]):
        index = next((index for index, classroom in enumerate(self.classrooms) if classroom.id == id), None)
        if index is not None:
            self.classrooms[index] = Classroom(**data)
    
    def generate_id(self) -> int:
        return len(self.classrooms) + 1

class TestClassroomsOperations:

    def test_get_classrooms(self):
        # Given
        classrooms = [Classroom(id=1, students_ids=[1, 2], subject_id=1), Classroom(id=2, students_ids=[3,4], subject_id=1)]
        classroom_storage = MockClassroomStorage(classrooms)
        classrooms_operations = ClassroomsOperations(classroom_storage)
        want = classrooms

        # When
        got = classrooms_operations.get_classrooms()

        # Then
        assert got == want

    def test_get_classrooms_empty_list_when_no_classrooms(self):
        # Given
        classroom_storage = MockClassroomStorage([])
        classrooms_operations = ClassroomsOperations(classroom_storage)
        want = []

        # When
        got = classrooms_operations.get_classrooms()

        # Then
        assert got == want

    def test_add_classroom(self):
        # Given
        classroom = BaseClassroom(students_ids=[1, 2], subject_id=1)
        classroom_storage = MockClassroomStorage([])
        classrooms_operations = ClassroomsOperations(classroom_storage)
        want = Classroom(id=1, **classroom.model_dump())

        # When
        got = classrooms_operations.add_classroom(classroom)

        # Then
        assert got == want
    
    def test_delete_classroom(self):
        # Given
        classroom = Classroom(id=1, students_ids=[1, 2], subject_id=1)
        classroom_storage = MockClassroomStorage([classroom])
        classrooms_operations = ClassroomsOperations(classroom_storage)
        want = []

        # When
        classrooms_operations.delete_classroom(1)

        # Then
        assert classroom_storage.classrooms == want

    def test_delete_classroom_when_classroom_does_not_exist(self):
        # Given
        classroom_storage = MockClassroomStorage([])
        classrooms_operations = ClassroomsOperations(classroom_storage)
        want = []

        # When
        classrooms_operations.delete_classroom(1)

        # Then
        assert classroom_storage.classrooms == want

    def test_update_classroom(self):
        # Given
        classroom = Classroom(id=1, students_ids=[1, 2], subject_id=1)
        classroom_storage = MockClassroomStorage([classroom])
        classrooms_operations = ClassroomsOperations(classroom_storage)
        want = BaseClassroom(students_ids=[3, 4], subject_id=1)

        # When
        classrooms_operations.update_classroom(1, want)

        # Then
        assert classroom_storage.classrooms[0] == Classroom(id=1, **want.model_dump())

    def test_update_classroom_when_classroom_does_not_exist(self):
        # Given
        classroom_storage = MockClassroomStorage([])
        classrooms_operations = ClassroomsOperations(classroom_storage)
        want = BaseClassroom(students_ids=[3, 4], subject_id=1)

        # When
        classrooms_operations.update_classroom(1, want)

        # Then
        assert classroom_storage.classrooms == []
