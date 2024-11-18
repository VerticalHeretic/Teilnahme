from typing import Any, Dict, List

import pytest

from src.common.models import DegreeName, Subject
from src.common.storage.storage import StorageHandler
from src.modules.subjects_operations import SubjectDataError, SubjectsOperations


class MockSubjectsStorage(StorageHandler):
    def __init__(self, subjects: List[Subject]):
        self.subjects = subjects

    def save(self, data: Dict[str, Any]):
        self.subjects.append(Subject(**data))

    def load(self) -> List[Dict[str, Any]]:
        return [s.model_dump() for s in self.subjects]

    def delete(self, id: int):
        self.subjects = [s for s in self.subjects if s.id != id]

    def update(self, id: int, data: Dict[str, Any]):
        index = next(
            (index for index, subject in enumerate(self.subjects) if subject.id == id),
            None,
        )

        if index is not None:
            self.subjects[index] = Subject(**data)

    def generate_id(self) -> int:
        return len(self.subjects) + 1


class TestSubjectsOperations:
    def test_get_subjects(self):
        # Given
        subject = Subject(id=1, name="Math", semester=4, degree=DegreeName.bachelor)
        subjects_storage = MockSubjectsStorage([subject])
        subjects_operations = SubjectsOperations(subjects_storage)
        want = [subject]

        # When
        got = subjects_operations.get_subjects()

        # Then
        assert got == want

    def test_get_empty_list_when_no_subjects(self):
        # Given
        subjects_storage = MockSubjectsStorage([])
        subjects_operations = SubjectsOperations(subjects_storage)
        want = []

        # When
        got = subjects_operations.get_subjects()

        # Then
        assert got == want

    def test_get_subjects_raises_error_when_invalid_subject_data(self):
        # Given
        subject = Subject(name="Math", semester=4, degree=DegreeName.bachelor)
        subjects_storage = MockSubjectsStorage([subject])
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        with pytest.raises(SubjectDataError):
            subjects_operations.get_subjects()

    def test_add_subject(self):
        # Given
        subject = Subject(name="Math", semester=4, degree=DegreeName.bachelor)
        subjects_storage = MockSubjectsStorage([])
        subjects_operations = SubjectsOperations(subjects_storage)
        want = Subject(id=1, name="Math", semester=4, degree=DegreeName.bachelor)

        # When
        got = subjects_operations.add_subject(subject)

        # Then
        assert got == want
        assert subjects_storage.subjects == [want]

    def test_delete_subject(self):
        # Given
        subject = Subject(id=1, name="Math", semester=4, degree=DegreeName.bachelor)
        subjects_storage = MockSubjectsStorage([subject])
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        subjects_operations.delete_subject(1)

        # Then
        assert subjects_storage.subjects == []

    def test_delete_non_existing_subject(self):
        # Given
        subjects_storage = MockSubjectsStorage([])
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        subjects_operations.delete_subject(1)

        # Then
        assert subjects_storage.subjects == []

    def test_update_subject(self):
        # Given
        subject = Subject(id=1, name="Math", semester=4, degree=DegreeName.bachelor)
        subjects_storage = MockSubjectsStorage([subject])
        subjects_operations = SubjectsOperations(subjects_storage)
        want = Subject(id=1, name="Physics", semester=4, degree=DegreeName.bachelor)

        # When
        subjects_operations.update_subject(
            1, Subject(name="Physics", semester=4, degree=DegreeName.bachelor)
        )

        # Then
        assert subjects_storage.subjects == [want]

    def test_update_non_existing_subject(self):
        # Given
        subjects_storage = MockSubjectsStorage([])
        subjects_operations = SubjectsOperations(subjects_storage)

        # When
        subjects_operations.update_subject(
            1, Subject(name="Physics", semester=4, degree=DegreeName.bachelor)
        )

        # Then
        assert subjects_storage.subjects == []
