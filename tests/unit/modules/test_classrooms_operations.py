import pytest
from sqlmodel import Session, SQLModel, create_engine

from src.common.errors import NotFoundError
from src.common.models import Classroom, DegreeName, Student
from src.common.storage.db_storage import DBStorageHandler
from src.modules.classrooms_operations import ClassroomsOperations

example_students: list[Student] = [
    Student(id=1, name="John", surname="Daw", degree=DegreeName.bachelor, semester=4),
    Student(id=2, name="Joe", surname="Daw", degree=DegreeName.bachelor, semester=4),
    Student(id=3, name="Hank", surname="Daw", degree=DegreeName.bachelor, semester=4),
]


@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        for student in example_students:
            session.add(student)
        session.commit()
        yield session


class TestClassroomsOperations:
    def test_get_classrooms(self, test_db):
        # Given
        want = [
            Classroom(id=1, students_ids=example_students, subject_id=1),
            Classroom(id=2, students_ids=example_students, subject_id=2),
        ]
        classroom_storage = DBStorageHandler(test_db)
        for classroom in want:
            test_db.add(classroom)
        test_db.commit()
        classrooms_operations = ClassroomsOperations(classroom_storage)

        # When
        got = classrooms_operations.get_classrooms()

        # Then
        assert got == want

    def test_get_classrooms_empty_list_when_no_classrooms(self, test_db):
        # Given
        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(classroom_storage)
        want = []

        # When
        got = classrooms_operations.get_classrooms()

        # Then
        assert got == want

    def test_add_classroom(self, test_db):
        # Given
        classroom = Classroom(students=example_students, subject_id=1)
        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(classroom_storage)

        # When
        got = classrooms_operations.add_classroom(classroom)

        # Then
        assert got == classroom

    def test_delete_classroom(self, test_db):
        # Given
        classroom = Classroom(id=1, students=example_students, subject_id=1)
        classroom_storage = DBStorageHandler(test_db)
        test_db.add(classroom)
        test_db.commit()
        classrooms_operations = ClassroomsOperations(classroom_storage)
        want = []

        # When
        classrooms_operations.delete_classroom(1)

        # Then
        assert classroom_storage.classrooms == want

    def test_delete_classroom_when_classroom_does_not_exist(self, test_db):
        # Given
        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(classroom_storage)
        want = []

        # When
        classrooms_operations.delete_classroom(1)

        # Then
        assert classroom_storage.classrooms == want

    def test_update_classroom(self, test_db):
        # Given
        classroom = Classroom(id=1, students_ids=example_students, subject_id=1)
        classroom_storage = DBStorageHandler(test_db)
        test_db.add(classroom)
        test_db.commit()
        classrooms_operations = ClassroomsOperations(classroom_storage)
        want = Classroom(id=1, students_ids=example_students, subject_id=2)

        # When
        classrooms_operations.update_classroom(classroom.id, want)

        # Then
        assert test_db.get(Classroom, 1) == want

    def test_update_classroom_when_classroom_does_not_exist(self, test_db):
        # Given
        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(classroom_storage)

        # Then
        with pytest.raises(NotFoundError):
            classrooms_operations.update_classroom(
                1, Classroom(id=1, students=example_students, subject_id=2)
            )
