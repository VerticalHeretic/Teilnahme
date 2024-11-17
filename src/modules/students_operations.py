from typing import Annotated, List

from fastapi import Depends
from src.common.models import Student
from src.common.storage.db_storage import DBStorageHandlerDep
from src.common.storage.storage import NewStorageHandler
from src.common.errors import NotFoundError

class StudentsOperations:
    """Class for managing student operations.
    
    This class provides methods for CRUD operations on students using a storage handler.
    """

    def __init__(self, storage_handler: NewStorageHandler):
        """Initialize StudentsOperations with a storage handler.
        
        Args:
            storage_handler (StorageHandler): Handler for student data storage operations
        """
        self.storage_handler = storage_handler

    def get_students(self) -> List[Student]:
        """Get list of all students
        
        Returns:
            List[Student]: List of students

        Raises: 
            StudentDataError: When student data is invalid
        """
        return self.storage_handler.get_all(Student)

    def add_student(self, student: Student) -> Student:
        # TODO: Will need to check if the student is valid (i.e. if the degree is valid, if the semester is valid, etc.)

        """Add student to storage
        
        Args:
            student (Student): Student to add
        """
        self.storage_handler.create(student)

        return student

    def delete_student(self, id: int):
        """Delete student from storage
        
        Args:
            id (int): Student id
        """
        
        try:
            self.storage_handler.delete(id, Student)
        except ValueError:
            raise NotFoundError(f"Student with id {id} not found")

    def update_student(self, id: int, updated_student: Student) -> Student:
        """Update student in storage
        
        Args:
            id (int): Student id
            updated_student (Student): Updated student data
        """

        try:
            self.storage_handler.update(id, updated_student)
        except ValueError:
            raise NotFoundError(f"Student with id {id} not found")
        return updated_student

def get_students_operations_with_db_storage_handler(db_storage_handler: DBStorageHandlerDep) -> StudentsOperations:
    return StudentsOperations(db_storage_handler)

StudentsOperationsDep = Annotated[StudentsOperations, Depends(get_students_operations_with_db_storage_handler)]