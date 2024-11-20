from typing import List

from src.common.errors import NotFoundError
from src.common.models import Classroom
from src.common.storage.storage import NewStorageHandler


class ClassroomsOperations:
    """Class for managing classroom operations.

    This class provides methods for CRUD operations on classrooms using a storage handler.
    """

    def __init__(self, storage_handler: NewStorageHandler):
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
        return self.storage_handler.get_all(Classroom)

    def add_classroom(self, classroom: Classroom) -> Classroom:
        """Add a new classroom.

        Args:
            classroom (BaseClassroom): Classroom data to add

        Returns:
            Classroom: The newly created classroom with generated ID
        """
        return self.storage_handler.create(classroom)

    def delete_classroom(self, id: int):
        """Delete a classroom by ID.

        Args:
            id (int): ID of the classroom to delete
        """

        try:
            self.storage_handler.delete(id, Classroom)
        except ValueError:
            raise NotFoundError(f"Classroom with ID {id} not found")

    def update_classroom(self, id: int, updated_classroom: Classroom) -> Classroom:
        """Update an existing classroom.

        Args:
            id (int): ID of the classroom to update
            updated_classroom (BaseClassroom): New classroom data

        Returns:
            Classroom: The updated classroom
        """

        try:
            self.storage_handler.update(id, updated_classroom)
        except ValueError:
            raise NotFoundError(f"Classroom with ID {id} not found")

        return updated_classroom
