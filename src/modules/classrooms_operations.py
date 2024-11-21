from typing import List

from src.common.errors import NotFoundError
from src.common.models import Classroom, Student
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

    def add_students_to_classroom(self, classroom_id: int, students: List[Student]):
        """Add students to a classroom.

        Args:
            classroom_id (int): ID of the classroom to add students to
            students (List[Student]): List of students to add
        """
        try:
            classroom = self.storage_handler.get_by_id(classroom_id, Classroom)
            classroom.students.extend(students)
            return self.storage_handler.update(classroom_id, classroom)
        except ValueError:
            raise NotFoundError(f"Classroom with ID {classroom_id} not found")

    def delete_student_from_classroom(self, classroom_id: int, student_id: int):
        try:
            classroom = self.storage_handler.get_by_id(classroom_id, Classroom)
            classroom.students = [
                student for student in classroom.students if student.id != student_id
            ]
            return self.storage_handler.update(classroom_id, classroom)
        except ValueError:
            raise NotFoundError(f"Classroom with ID {classroom_id} not found")

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
