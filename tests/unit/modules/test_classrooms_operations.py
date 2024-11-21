import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.common.errors import NotFoundError
from src.common.models import Classroom, DegreeName, Student
from src.common.storage.db_storage import DBStorageHandler
from src.modules.classrooms_operations import ClassroomsOperations

example_students: list[Student] = [
    Student(name="John", surname="Daw", degree=DegreeName.bachelor, semester=4),
    Student(name="Joe", surname="Daw", degree=DegreeName.bachelor, semester=4),
    Student(name="Hank", surname="Daw", degree=DegreeName.bachelor, semester=4),
]


@pytest.fixture
def test_db():
    engine = create_engine(
        "sqlite://",  # In-memory SQLite database URL - creates temporary database that exists only during test execution
        connect_args={
            "check_same_thread": False
        },  # SQLite-specific setting that allows multiple threads to access the same connection
        poolclass=StaticPool,  # Uses a single connection for all operations - ideal for testing as it maintains consistent state
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestClassroomsOperations:
    def test_get_classrooms(self, test_db):
        # Given
        want = [
            Classroom(students=example_students, subject_id=1),
            Classroom(students=example_students, subject_id=2),
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
        students = [
            Student(name="John", surname="Daw", degree=DegreeName.bachelor, semester=4),
            Student(name="Joe", surname="Daw", degree=DegreeName.bachelor, semester=4),
            Student(name="Hank", surname="Daw", degree=DegreeName.bachelor, semester=4),
        ]

        for student in students:
            test_db.add(student)
            test_db.commit()
            test_db.refresh(student)

        classroom = Classroom(students=students, subject_id=1)
        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(classroom_storage)

        # When
        got = classrooms_operations.add_classroom(classroom)

        # Then
        assert got == classroom
        # Ensure the classroom is persisted
        assert test_db.get(Classroom, got.id) is not None

    def test_delete_classroom(self, test_db):
        # Given
        student = Student(
            name="John", surname="Daw", degree=DegreeName.bachelor, semester=4
        )
        test_db.add(student)
        test_db.commit()
        test_db.refresh(student)

        classroom = Classroom(students=[student], subject_id=1)
        classroom_storage = DBStorageHandler(test_db)
        test_db.add(classroom)
        test_db.commit()
        classrooms_operations = ClassroomsOperations(classroom_storage)

        # When
        classrooms_operations.delete_classroom(1)

        # Then
        assert test_db.get(Classroom, 1) is None

    def test_delete_classroom_when_classroom_does_not_exist(self, test_db):
        # Given
        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(classroom_storage)

        # When / Then
        with pytest.raises(NotFoundError):
            classrooms_operations.delete_classroom(1)

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
