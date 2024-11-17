from typing import Annotated, List

from fastapi import Depends

from src.common.errors import NotFoundError
from src.common.models import DegreeName, Student
from src.common.storage.db_storage import DBStorageHandlerDep
from src.common.storage.storage import NewStorageHandler


class StudentBachelorSemesterError(Exception):
    """Exception raised for errors in student bachelor semester."""

    pass


class StudentMasterSemesterError(Exception):
    """Exception raised for errors in student master semester."""

    pass


class StudentsOperations:
    """Class for managing student operations.

    This class provides methods for CRUD operations on students using a storage handler.
    """

    def __init__(self, storage_handler: NewStorageHandler):
        """Initialize StudentsOperations with a storage handler.

        Args:
            storage_handler (NewStorageHandler): Handler for student data storage operations
        """
        self.storage_handler = storage_handler

    def get_students(self) -> List[Student]:
        """Get list of all students.

        Returns:
            List[Student]: List of all students in storage
        """
        return self.storage_handler.get_all(Student)

    def get_students_in_degree(
        self, degree_name: DegreeName, semester: int | None = None
    ) -> List[Student]:
        """Get list of all students in a given degree and semester.

        Args:
            degree_name (DegreeName): Degree name
            semester (int | None): Semester number (optional)

        Returns:
            List[Student]: List of all students in the specified degree and semester
        """
        if (
            degree_name is DegreeName.bachelor
            and isinstance(semester, int)
            and semester > 6
        ):
            raise StudentBachelorSemesterError("Bachelor degree has only 6 semesters")
        elif (
            degree_name is DegreeName.master
            and isinstance(semester, int)
            and semester > 4
        ):
            raise StudentMasterSemesterError("Master degree has only 4 semesters")

        conditions = [Student.degree == degree_name]
        if semester is not None:
            conditions.append(Student.semester == semester)
        return self.storage_handler.get_all_where(Student, conditions)

    def get_student(self, id: int) -> Student:
        """Get a student by their ID.

        Args:
            id (int): ID of the student to retrieve

        Returns:
            Student: The student with the specified ID

        Raises:
            NotFoundError: When student with given ID is not found
        """
        try:
            return self.storage_handler.get_by_id(id, Student)
        except ValueError:
            raise NotFoundError(f"Student with id {id} not found")

    def add_student(self, student: Student) -> Student:
        """Add a new student to storage.

        Args:
            student (Student): Student data to add

        Returns:
            Student: The newly created student

        Note:
            TODO: Will need to check if the student is valid (i.e. if the degree is valid, if the semester is valid, etc.)
        """
        self.storage_handler.create(student)
        return student

    def delete_student(self, id: int):
        """Delete a student from storage.

        Args:
            id (int): ID of the student to delete

        Raises:
            NotFoundError: When student with given ID is not found
        """
        try:
            self.storage_handler.delete(id, Student)
        except ValueError:
            raise NotFoundError(f"Student with id {id} not found")

    def update_student(self, id: int, updated_student: Student) -> Student:
        """Update an existing student in storage.

        Args:
            id (int): ID of the student to update
            updated_student (Student): New student data

        Returns:
            Student: The updated student

        Raises:
            NotFoundError: When student with given ID is not found
        """
        try:
            self.storage_handler.update(id, updated_student)
        except ValueError:
            raise NotFoundError(f"Student with id {id} not found")
        return updated_student


def get_students_operations_with_db_storage_handler(
    db_storage_handler: DBStorageHandlerDep,
) -> StudentsOperations:
    """Create a StudentsOperations instance with a database storage handler.

    Args:
        db_storage_handler (DBStorageHandlerDep): Database storage handler dependency

    Returns:
        StudentsOperations: New StudentsOperations instance configured with the database handler
    """
    return StudentsOperations(db_storage_handler)


StudentsOperationsDep = Annotated[
    StudentsOperations, Depends(get_students_operations_with_db_storage_handler)
]
