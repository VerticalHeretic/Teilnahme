import pytest

from src.common.errors import NotFoundError
from src.common.models import Classroom, DegreeName, Student
from src.common.storage.db_storage import DBStorageHandler
from src.modules.classrooms_operations import ClassroomsOperations
from src.modules.students_operations import StudentsOperations

example_students: list[Student] = [
    Student(name="John", surname="Daw", degree=DegreeName.bachelor, semester=4),
    Student(name="Joe", surname="Daw", degree=DegreeName.bachelor, semester=4),
    Student(name="Hank", surname="Daw", degree=DegreeName.bachelor, semester=4),
]


@pytest.fixture
def test_students_operations(test_db) -> StudentsOperations:
    storage_handler = DBStorageHandler(test_db)
    return StudentsOperations(storage_handler)


class TestClassroomsOperations:
    def test_get_classrooms(self, test_db, test_students_operations):
        # Given
        want = [
            Classroom(students=example_students, subject_id=1),
            Classroom(students=example_students, subject_id=2),
        ]
        classroom_storage = DBStorageHandler(test_db)
        for classroom in want:
            test_db.add(classroom)
        test_db.commit()
        classrooms_operations = ClassroomsOperations(
            classroom_storage, test_students_operations
        )

        # When
        got = classrooms_operations.get_classrooms()

        # Then
        assert got == want

    def test_get_classrooms_empty_list_when_no_classrooms(
        self, test_db, test_students_operations
    ):
        # Given
        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(
            classroom_storage, test_students_operations
        )
        want = []

        # When
        got = classrooms_operations.get_classrooms()

        # Then
        assert got == want

    def test_add_classroom(self, test_db, test_students_operations):
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
        classrooms_operations = ClassroomsOperations(
            classroom_storage, test_students_operations
        )

        # When
        got = classrooms_operations.add_classroom(classroom)

        # Then
        assert got == classroom
        # Ensure the classroom is persisted
        assert test_db.get(Classroom, got.id) is not None

    def test_add_students_to_classroom(self, test_db, test_students_operations):
        # Given
        classroom = Classroom(subject_id=1)
        test_db.add(classroom)
        test_db.commit()
        test_db.refresh(classroom)

        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(
            classroom_storage, test_students_operations
        )
        student = Student(
            name="John", surname="Daw", degree=DegreeName.bachelor, semester=4
        )

        # When
        got = classrooms_operations.add_students_to_classroom(classroom.id, [student])

        # Then
        assert got.students == [student]

    def test_add_students_to_classroom_when_classroom_does_not_exist(
        self, test_db, test_students_operations
    ):
        # Given
        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(
            classroom_storage, test_students_operations
        )

        # Then
        with pytest.raises(NotFoundError):
            classrooms_operations.add_students_to_classroom(1, [Student()])

    def test_delete_student_from_classroom(self, test_db, test_students_operations):
        # Given
        student = Student(
            name="John", surname="Daw", degree=DegreeName.bachelor, semester=4
        )
        classroom = Classroom(students=[student], subject_id=1)
        test_db.add(classroom)
        test_db.commit()
        test_db.refresh(classroom)

        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(
            classroom_storage, test_students_operations
        )

        # When
        got = classrooms_operations.delete_student_from_classroom(
            classroom.id, student.id
        )

        # Then
        assert got.students == []

    def test_delete_student_from_classroom_when_classroom_does_not_exist(
        self, test_db, test_students_operations
    ):
        # Given
        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(
            classroom_storage, test_students_operations
        )

        # Then
        with pytest.raises(NotFoundError):
            classrooms_operations.delete_student_from_classroom(1, 1)

    def test_delete_classroom(self, test_db, test_students_operations):
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
        classrooms_operations = ClassroomsOperations(
            classroom_storage, test_students_operations
        )

        # When
        classrooms_operations.delete_classroom(1)

        # Then
        assert test_db.get(Classroom, 1) is None

    def test_delete_classroom_when_classroom_does_not_exist(
        self, test_db, test_students_operations
    ):
        # Given
        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(
            classroom_storage, test_students_operations
        )

        # When / Then
        with pytest.raises(NotFoundError):
            classrooms_operations.delete_classroom(1)

    def test_update_classroom(self, test_db, test_students_operations):
        # Given
        classroom = Classroom(id=1, students_ids=example_students, subject_id=1)
        classroom_storage = DBStorageHandler(test_db)
        test_db.add(classroom)
        test_db.commit()
        classrooms_operations = ClassroomsOperations(
            classroom_storage, test_students_operations
        )
        want = Classroom(id=1, students_ids=example_students, subject_id=2)

        # When
        classrooms_operations.update_classroom(classroom.id, want)

        # Then
        assert test_db.get(Classroom, 1) == want

    def test_update_classroom_when_classroom_does_not_exist(
        self, test_db, test_students_operations
    ):
        # Given
        classroom_storage = DBStorageHandler(test_db)
        classrooms_operations = ClassroomsOperations(
            classroom_storage, test_students_operations
        )

        # Then
        with pytest.raises(NotFoundError):
            classrooms_operations.update_classroom(
                1, Classroom(id=1, students=example_students, subject_id=2)
            )
