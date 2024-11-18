from typing import Annotated, List

from fastapi import Depends

from src.common.errors import NotFoundError
from src.common.models import DegreeName, Student
from src.common.storage.db_storage import DBStorageHandlerDep
from src.common.storage.storage import NewStorageHandler


class SemesterError(Exception):
    """Exception raised when a student's semester number is invalid.
    
    This includes cases where:
    - Bachelor semester is greater than 6
    - Master semester is greater than 4 
    - Semester is less than or equal to 0
    """

    pass


class StudentValidationError(Exception):
    """Exception raised when student data is invalid.
    
    This includes cases where:
    - Name is less than 2 characters
    - Surname is less than 2 characters
    """

    pass


class StudentsOperations:
    """Class for managing student operations.

    This class provides methods for CRUD (Create, Read, Update, Delete) operations on students 
    using a storage handler. It includes validation of student data and semester numbers.

    Attributes:
        storage_handler (NewStorageHandler): Handler for student data storage operations
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
        """Get list of all students in a given degree and optionally filtered by semester.

        Args:
            degree_name (DegreeName): Name of the degree program (bachelor/master)
            semester (int | None, optional): Semester number to filter by. Defaults to None.

        Returns:
            List[Student]: List of students matching the criteria

        Raises:
            SemesterError: If the specified semester is invalid for the degree
        """
        conditions = [Student.degree == degree_name]
        if semester is not None:
            self._validate_semester(degree_name, semester)
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

        Raises:
            StudentValidationError: If student data is invalid
            SemesterError: If semester number is invalid for the degree
        """
        self._validate_student(student)
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

    def _validate_semester(self, degree_name: DegreeName, semester: int):
        """Validate that a semester number is valid for a given degree.

        Args:
            degree_name (DegreeName): Name of the degree program
            semester (int): Semester number to validate

        Raises:
            SemesterError: If semester number is invalid for the degree
        """
        if degree_name == DegreeName.bachelor and semester > 6:
            raise SemesterError("Bachelor degree has only 6 semesters")
        elif degree_name == DegreeName.master and semester > 4:
            raise SemesterError("Master degree has only 4 semesters")
        elif semester <= 0:
            raise SemesterError("Semester number must be greater than 0")

    def _validate_student(self, student: Student):
        """Validate student data.

        Checks:
        - Semester number is valid for the degree
        - Name and surname are at least 2 characters long

        Args:
            student (Student): Student data to validate

        Raises:
            StudentValidationError: If student data is invalid
            SemesterError: If semester number is invalid for the degree
        """
        self._validate_semester(student.degree, student.semester)

        if len(student.name) < 2 or len(student.surname) < 2:
            raise StudentValidationError(
                "Name and surname must be at least 2 characters long"
            )


def get_students_operations_with_db_storage_handler(
    db_storage_handler: DBStorageHandlerDep,
) -> StudentsOperations:
    """Create a StudentsOperations instance with a database storage handler.

    This is a FastAPI dependency that creates a StudentsOperations instance
    configured with a database storage handler.

    Args:
        db_storage_handler (DBStorageHandlerDep): Database storage handler dependency

    Returns:
        StudentsOperations: New StudentsOperations instance configured with the database handler
    """
    return StudentsOperations(db_storage_handler)


StudentsOperationsDep = Annotated[
    StudentsOperations, Depends(get_students_operations_with_db_storage_handler)
]
