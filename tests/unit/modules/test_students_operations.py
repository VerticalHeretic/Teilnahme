import pytest
from sqlmodel import Session, SQLModel, create_engine

from src.common.errors import NotFoundError, SemesterError
from src.common.models import DegreeName, Student
from src.common.storage.db_storage import DBStorageHandler
from src.modules.students_operations import (
    StudentsOperations,
    StudentValidationError,
)


@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestStudentsOperations:
    def test_get_students(self, test_db):
        # Given

        student = Student(
            id=1, name="John", surname="Daw", degree=DegreeName.bachelor, semester=4
        )

        test_db.add(student)
        test_db.commit()
        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)
        want = [student]

        # When
        got = students_operations.get_students()

        # Then
        assert got == want

    def test_get_empty_list_when_no_students(self, test_db):
        # Given
        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)
        want = []

        # When
        got = students_operations.get_students()

        # Then
        assert got == want

    def test_get_students_in_degree(self, test_db):
        # Given
        students = [
            Student(
                id=1, name="John", surname="Daw", degree=DegreeName.bachelor, semester=4
            ),
            Student(
                id=2,
                name="Jane",
                surname="Smith",
                degree=DegreeName.bachelor,
                semester=6,
            ),
            Student(
                id=3,
                name="Alice",
                surname="Johnson",
                degree=DegreeName.master,
                semester=2,
            ),
        ]
        for student in students:
            test_db.add(student)
        test_db.commit()

        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)
        want = students[:2]

        # When
        got = students_operations.get_students_in_degree(DegreeName.bachelor)

        # Then
        assert got == want

    def test_get_students_in_degree_with_semester(self, test_db):
        # Given
        students = [
            Student(
                id=1, name="John", surname="Daw", degree=DegreeName.bachelor, semester=4
            ),
            Student(
                id=2,
                name="Jane",
                surname="Smith",
                degree=DegreeName.bachelor,
                semester=6,
            ),
            Student(
                id=3,
                name="Alice",
                surname="Johnson",
                degree=DegreeName.master,
                semester=2,
            ),
        ]
        for student in students:
            test_db.add(student)
        test_db.commit()

        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)
        want = [students[0]]

        # When
        got = students_operations.get_students_in_degree(DegreeName.bachelor, 4)

        # Then
        assert got == want

    def test_get_students_in_degree_with_invalid_semester(self, test_db):
        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)

        # When
        with pytest.raises(SemesterError):
            students_operations.get_students_in_degree(DegreeName.bachelor, 10)

        with pytest.raises(SemesterError):
            students_operations.get_students_in_degree(DegreeName.master, 10)

        with pytest.raises(SemesterError):
            students_operations.get_students_in_degree(DegreeName.bachelor, 0)

    def test_add_student(self, test_db):
        # Given
        student = Student(
            name="John", surname="Daw", degree=DegreeName.bachelor, semester=4
        )
        test_db.add(student)
        test_db.commit()

        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)

        # When
        students_operations.add_student(student)

        # Then
        assert student == test_db.get(Student, 1)

    def test_add_student_with_invalid_semester(self, test_db):
        # Given
        student = Student(
            name="John", surname="Daw", degree=DegreeName.bachelor, semester=10
        )
        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)

        # When
        with pytest.raises(SemesterError):
            students_operations.add_student(student)

    def test_add_student_with_invalid_name(self, test_db):
        # Given
        student = Student(
            name="", surname="Daw", degree=DegreeName.bachelor, semester=4
        )
        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)

        # When
        with pytest.raises(StudentValidationError):
            students_operations.add_student(student)

    def test_add_student_with_invalid_surname(self, test_db):
        # Given
        student = Student(
            name="John", surname="", degree=DegreeName.bachelor, semester=4
        )
        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)

        # When
        with pytest.raises(StudentValidationError):
            students_operations.add_student(student)

    def test_delete_student(self, test_db):
        # Given
        student = Student(
            id=1, name="John", surname="Daw", degree=DegreeName.bachelor, semester=4
        )
        test_db.add(student)
        test_db.commit()
        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)

        # When
        students_operations.delete_student(student.id)

        # Then
        assert test_db.get(Student, 1) is None

    def test_delete_student_with_invalid_id(self, test_db):
        # Given
        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)

        # When
        with pytest.raises(NotFoundError):
            students_operations.delete_student(1)

    def test_update_student(self, test_db):
        # Given
        student = Student(
            id=1, name="John", surname="Daw", degree=DegreeName.bachelor, semester=4
        )
        test_db.add(student)
        test_db.commit()

        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)

        updated_student = Student(
            id=1, name="Jane", surname="Smith", degree=DegreeName.bachelor, semester=6
        )

        # When
        students_operations.update_student(student.id, updated_student)

        # Then
        assert test_db.get(Student, 1) == updated_student

    def test_update_student_with_invalid_id(self, test_db):
        # Given
        students_storage = DBStorageHandler(session=test_db)
        students_operations = StudentsOperations(students_storage)

        # When
        with pytest.raises(NotFoundError):
            students_operations.update_student(
                1,
                Student(
                    id=1,
                    name="Jane",
                    surname="Smith",
                    degree=DegreeName.bachelor,
                    semester=6,
                ),
            )
