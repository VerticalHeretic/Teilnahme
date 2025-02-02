from dataclasses import dataclass
from typing import List

from src.common.errors import NotFoundError
from src.common.models import DegreeName, Subject
from src.common.storage.storage import NewStorageHandler
from src.common.validators import validate_semester


class SubjectValidationError(Exception):
    """Exception raised for errors in subject data.

    This includes cases where:
    - Subject name is less than 2 characters long
    """

    pass


@dataclass
class SubjectsOperations:
    """Class for managing subject operations.

    This class provides methods for CRUD (Create, Read, Update, Delete) operations on subjects
    using a storage handler. It includes validation of subject data and semester numbers.

    Attributes:
        storage_handler (NewStorageHandler): Handler for subject data storage operations
    """

    storage_handler: NewStorageHandler

    def get_subjects(self) -> List[Subject]:
        """Get list of all subjects.

        Returns:
            List[Subject]: List of all subjects in storage
        """
        return self.storage_handler.get_all(Subject)

    def get_subject(self, id: int) -> Subject:
        """Get a subject by its ID.

        Args:
            id (int): ID of the subject to retrieve

        Returns:
            Subject: The subject with the specified ID

        Raises:
            NotFoundError: When subject with given ID is not found
        """
        try:
            return self.storage_handler.get_by_id(id, Subject)
        except ValueError:
            raise NotFoundError(f"Subject with id {id} not found")

    def get_subjects_in_degree(
        self, degree_name: DegreeName, semester: int | None = None
    ) -> List[Subject]:
        """Get list of all subjects in a given degree and optionally filtered by semester.

        Args:
            degree_name (DegreeName): Name of the degree program (bachelor/master)
            semester (int | None, optional): Semester number to filter by. Defaults to None.

        Returns:
            List[Subject]: List of subjects matching the criteria

        Raises:
            SemesterError: If the specified semester is invalid for the degree
        """
        conditions = [Subject.degree == degree_name]
        if semester is not None:
            validate_semester(degree_name, semester)
            conditions.append(Subject.semester == semester)

        return self.storage_handler.get_all_where(Subject, conditions)

    def add_subject(self, subject: Subject) -> Subject:
        """Add a new subject to storage.

        Args:
            subject (Subject): Subject data to add

        Returns:
            Subject: The newly created subject

        Raises:
            SubjectValidationError: If subject data is invalid
            SemesterError: If semester number is invalid for the degree
        """
        self._validate_subject(subject)
        self.storage_handler.create(subject)
        return subject

    def delete_subject(self, id: int):
        """Delete a subject from storage.

        Args:
            id (int): ID of the subject to delete

        Raises:
            NotFoundError: When subject with given ID is not found
        """
        try:
            self.storage_handler.delete(id, Subject)
        except ValueError:
            raise NotFoundError(f"Subject with id {id} not found")

    def update_subject(self, id: int, updated_subject: Subject) -> Subject:
        """Update an existing subject in storage.

        Args:
            id (int): ID of the subject to update
            updated_subject (Subject): New subject data

        Returns:
            Subject: The updated subject

        Raises:
            NotFoundError: When subject with given ID is not found
            SubjectValidationError: If updated subject data is invalid
            SemesterError: If semester number is invalid for the degree
        """
        self._validate_subject(updated_subject)

        try:
            self.storage_handler.update(id, updated_subject)
        except ValueError:
            raise NotFoundError(f"Subject with id {id} not found")

        return updated_subject

    def _validate_subject(self, subject: Subject):
        """Validate subject data.

        Checks:
        - Semester number is valid for the degree
        - Name is at least 2 characters long

        Args:
            subject (Subject): Subject data to validate

        Raises:
            SubjectValidationError: If subject data is invalid
            SemesterError: If semester number is invalid for the degree
        """
        validate_semester(subject.degree, subject.semester)

        if len(subject.name) < 2:
            raise SubjectValidationError(
                "Subject name must be at least 2 characters long"
            )
