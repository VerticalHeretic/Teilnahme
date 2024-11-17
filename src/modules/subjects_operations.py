from src.common.storage.storage import StorageHandler
from src.common.models import Subject, BaseSubject
from typing import List
from pydantic import ValidationError


class SubjectDataError(Exception):
    """Exception raised for errors in subject data."""

    pass


class SubjectsOperations:
    """Class for managing subject operations.

    This class provides methods for CRUD operations on subjects using a storage handler.
    """

    def __init__(self, storage_handler: StorageHandler):
        """Initialize SubjectsOperations with a storage handler.

        Args:
            storage_handler (StorageHandler): Handler for subject data storage operations
        """
        self.storage_handler = storage_handler

    def get_subjects(self) -> List[Subject]:
        """Get list of all subjects.

        Returns:
            List[Subject]: List of all subjects

        Raises:
            SubjectDataError: When subject data is invalid
        """
        try:
            subjects = [
                Subject(**subject_data) for subject_data in self.storage_handler.load()
            ]
        except ValidationError as e:
            raise SubjectDataError(f"Invalid subject data format: {str(e)}") from e

        return subjects

    def add_subject(self, subject: BaseSubject) -> Subject:
        # TODO: Validate subject
        # TODO: Make the function async save

        """Add a new subject.

        Args:
            subject (BaseSubject): Subject data to add

        Returns:
            Subject: The newly created subject with generated ID
        """
        subject = Subject(id=self.storage_handler.generate_id(), **subject.model_dump())
        self.storage_handler.save(subject.model_dump())
        return subject

    def delete_subject(self, id: int):
        """Delete a subject by ID.

        Args:
            id (int): ID of the subject to delete
        """

        # TODO: Handle non-existing subject
        self.storage_handler.delete(id)

    def update_subject(self, id: int, updated_subject: BaseSubject) -> Subject:
        """Update an existing subject.

        Args:
            id (int): ID of the subject to update
            updated_subject (BaseSubject): New subject data

        Returns:
            Subject: The updated subject
        """
        updated_subject = Subject(id=id, **updated_subject.model_dump())
        # TODO: Handle non-existing subject
        self.storage_handler.update(id, updated_subject.model_dump())
        return updated_subject
