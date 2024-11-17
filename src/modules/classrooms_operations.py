from src.common.storage.storage import StorageHandler
from src.common.models import Classroom, BaseClassroom
from typing import List
from pydantic import ValidationError


class ClassroomDataError(Exception):
    """Exception raised for errors in classroom data."""

    pass


class ClassroomsOperations:
    """Class for managing classroom operations.

    This class provides methods for CRUD operations on classrooms using a storage handler.
    """

    def __init__(self, storage_handler: StorageHandler):
        """Initialize ClassroomsOperations with a storage handler.

        Args:
            storage_handler (StorageHandler): Handler for classroom data storage operations
        """
        self.storage_handler = storage_handler

    def get_classrooms(self) -> List[Classroom]:
        """Get list of all classrooms.

        Returns:
            List[Classroom]: List of all classrooms

        Raises:
            ClassroomDataError: When classroom data is invalid
        """
        try:
            classrooms = [
                Classroom(**classroom_data)
                for classroom_data in self.storage_handler.load()
            ]
        except ValidationError as e:
            raise ClassroomDataError(f"Invalid classroom data format: {str(e)}") from e

        return classrooms

    def add_classroom(self, classroom: BaseClassroom) -> Classroom:
        """Add a new classroom.

        Args:
            classroom (BaseClassroom): Classroom data to add

        Returns:
            Classroom: The newly created classroom with generated ID
        """
        classroom = Classroom(
            id=self.storage_handler.generate_id(), **classroom.model_dump()
        )
        self.storage_handler.save(classroom.model_dump())
        return classroom

    def delete_classroom(self, id: int):
        """Delete a classroom by ID.

        Args:
            id (int): ID of the classroom to delete
        """
        # TODO: Handle non-existing classroom check in delete
        self.storage_handler.delete(id)

    def update_classroom(self, id: int, updated_classroom: BaseClassroom) -> Classroom:
        """Update an existing classroom.

        Args:
            id (int): ID of the classroom to update
            updated_classroom (BaseClassroom): New classroom data

        Returns:
            Classroom: The updated classroom
        """
        updated_classroom = Classroom(id=id, **updated_classroom.model_dump())
        # TODO: Handle non-existing classroom check in update
        self.storage_handler.update(id, updated_classroom.model_dump())
        return updated_classroom
