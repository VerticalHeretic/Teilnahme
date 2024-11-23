import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from src.common.errors import NotFoundError, SemesterError
from src.common.models import DegreeName, Subject
from src.common.storage.db_storage import DBStorageHandler
from src.modules.subjects_operations import SubjectsOperations, SubjectValidationError


@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestSubjectsOperations:
    def test_get_subjects(self, test_db):
        # Given
        subject = Subject(id=1, name="Math", semester=4, degree=DegreeName.bachelor)
        test_db.add(subject)
        test_db.commit()
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)
        want = [subject]

        # When
        got = subjects_operations.get_subjects()

        # Then
        assert got == want

    def test_get_empty_list_when_no_subjects(self, test_db):
        # Given
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)
        want = []

        # When
        got = subjects_operations.get_subjects()

        # Then
        assert got == want

    def test_get_subject_by_id(self, test_db):
        # Given
        subject = Subject(id=1, name="Math", semester=4, degree=DegreeName.bachelor)
        test_db.add(subject)
        test_db.commit()
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        got = subjects_operations.get_subject(1)

        # Then
        assert got == subject

    def test_get_non_existing_subject(self, test_db):
        # Given
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        with pytest.raises(NotFoundError):
            subjects_operations.get_subject(1)

    def test_get_subjects_in_degree(self, test_db):
        # Given
        subjects = [
            Subject(id=1, name="Math", semester=4, degree=DegreeName.bachelor),
            Subject(id=2, name="Physics", semester=4, degree=DegreeName.master),
        ]
        for subject in subjects:
            test_db.add(subject)
        test_db.commit()
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        got = subjects_operations.get_subjects_in_degree(DegreeName.bachelor)

        # Then
        assert got == [subjects[0]]

    def test_get_subjects_in_degree_with_semester(self, test_db):
        subjects = [
            Subject(id=1, name="Math", semester=2, degree=DegreeName.bachelor),
            Subject(id=2, name="Physics", semester=4, degree=DegreeName.master),
        ]
        for subject in subjects:
            test_db.add(subject)
        test_db.commit()
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        got = subjects_operations.get_subjects_in_degree(DegreeName.bachelor, 2)

        # Then
        assert got == [subjects[0]]

    def test_add_subject(self, test_db):
        # Given
        subject = Subject(name="Math", semester=4, degree=DegreeName.bachelor)
        test_db.add(subject)
        test_db.commit()
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        got = subjects_operations.add_subject(subject)

        # Then
        assert got == subject

    def test_add_subject_invalid_semester(self, test_db):
        subject = Subject(name="Math", semester=10, degree=DegreeName.bachelor)
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)

        with pytest.raises(SemesterError):
            subjects_operations.add_subject(subject)

    def test_add_subject_invalid_name(self, test_db):
        subject = Subject(name="", semester=4, degree=DegreeName.bachelor)
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)

        with pytest.raises(SubjectValidationError):
            subjects_operations.add_subject(subject)

    def test_delete_subject(self, test_db):
        # Given
        subject = Subject(id=1, name="Math", semester=4, degree=DegreeName.bachelor)
        test_db.add(subject)
        test_db.commit()
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        subjects_operations.delete_subject(1)

        # Then
        assert test_db.exec(select(Subject)).all() == []

    def test_delete_non_existing_subject(self, test_db):
        # Given
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        with pytest.raises(NotFoundError):
            subjects_operations.delete_subject(1)

    def test_update_subject(self, test_db):
        # Given
        subject = Subject(id=1, name="Math", semester=4, degree=DegreeName.bachelor)
        test_db.add(subject)
        test_db.commit()
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        subjects_operations.update_subject(
            1, Subject(name="Physics", semester=4, degree=DegreeName.bachelor)
        )

        # Then
        assert test_db.get(Subject, 1) == subject

    def test_update_non_existing_subject(self, test_db):
        # Given
        subjects_storage = DBStorageHandler(session=test_db)
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        with pytest.raises(NotFoundError):
            subjects_operations.update_subject(
                1, Subject(name="Physics", semester=4, degree=DegreeName.bachelor)
            )
