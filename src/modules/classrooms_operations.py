from dataclasses import dataclass
from typing import List

from src.common.errors import NotFoundError
from src.common.models import Classroom, Student
from src.common.storage.storage import NewStorageHandler
from src.modules.students_operations import StudentsOperations


@dataclass
class ClassroomsOperations:
    """Class for managing classroom operations.

    This class provides methods for CRUD operations on classrooms using a storage handler.
    """

    storage_handler: NewStorageHandler
    students_operations: StudentsOperations

    def get_classrooms(self) -> List[Classroom]:
        """Get list of all classrooms.

        Returns:
            List[Classroom]: List of all classrooms

        Raises:
            ClassroomDataError: When classroom data is invalid
        """
        return self.storage_handler.get_all(Classroom)

    def get_classroom(self, id: int) -> Classroom:
        """Get a classroom by its ID.

        Args:
            id (int): ID of the classroom to retrieve

        Returns:
            Classroom: The classroom with the specified ID

        Raises:
            NotFoundError: When classroom with given ID is not found
        """
        try:
            return self.storage_handler.get_by_id(id, Classroom)
        except ValueError:
            raise NotFoundError(f"Classroom with ID {id} not found")

    def get_classrooms_for_subject(self, subject_id: int) -> List[Classroom]:
        """Get list of all classrooms for a given subject.

        Args:
            subject_id (int): ID of the subject to get classrooms for

        Returns:
            List[Classroom]: List of classrooms associated with the subject
        """
        return self.storage_handler.get_all_where(
            Classroom, [Classroom.subject_id == subject_id]
        )

    def get_classrooms_where_student(self, student_id: int) -> List[Classroom]:
        """Get list of all classrooms that contain a specific student.

        Args:
            student_id (int): ID of the student to find classrooms for

        Returns:
            List[Classroom]: List of classrooms that have the specified student enrolled
        """
        return self.storage_handler.get_all_where(
            Classroom, [Classroom.students.any(Student.id == student_id)]
        )

    def add_student_to_classroom(self, classroom_id: int, student_id: int):
        """Add a student to a classroom.

        Args:
            classroom_id (int): ID of the classroom to add student to
            student_id (int): ID of the student to add

        Returns:
            Classroom: The updated classroom with the student added

        Raises:
            NotFoundError: When either the student or classroom with given IDs is not found
        """
        try:
            student = self.students_operations.get_student(student_id)
            classroom = self.storage_handler.get_by_id(classroom_id, Classroom)
            classroom.students.append(student)
            return self.storage_handler.update(classroom_id, classroom)
        except ValueError:
            raise NotFoundError(
                f"Student with ID {student_id} or classroom with ID {classroom_id} not found"
            )

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
        """Delete a student from a classroom.

        Args:
            classroom_id (int): ID of the classroom to delete student from
            student_id (int): ID of the student to delete

        Returns:
            Classroom: The updated classroom with the student removed

        Raises:
            NotFoundError: When the classroom with given ID is not found
        """
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
