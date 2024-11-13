from typing import List
from src.common.models import BaseStudent, Student
from src.common.storage.storage import StorageHandler
from pydantic import ValidationError

class StudentDataError(Exception):
    """Raises when student data is invalid"""
    pass

class StudentsOperations:
    """Class for managing student operations.
    
    This class provides methods for CRUD operations on students using a storage handler.
    """

    def __init__(self, storage_handler: StorageHandler):
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

        try:
            students = [Student(**student_data) for student_data in self.storage_handler.load()]
        except ValidationError as e:
            raise StudentDataError(f"Invalid student data format: {str(e)}") from e

        return students

    def add_student(self, student: BaseStudent) -> Student:
        # TODO: Will need to check if the student is valid (i.e. if the degree is valid, if the semester is valid, etc.) 
        # TODO: Will need to make the function async save 

        """Add student to storage
        
        Args:
            student (Student): Student to add
        """
        student = Student(id=self.storage_handler.generate_id(), **student.model_dump())
        self.storage_handler.save(student.model_dump())
        return student

    def delete_student(self, id: int):
        """Delete student from storage
        
        Args:
            id (int): Student id
        """
        # TODO: Handle non-existing student 
        self.storage_handler.delete(id)

    def update_student(self, id: int, updated_student: BaseStudent) -> Student:
        """Update student in storage
        
        Args:
            id (int): Student id
            updated_student (Student): Updated student data
        """
        updated_student = Student(id=id, **updated_student.model_dump())
        # TODO: Handle non-existing student 
        self.storage_handler.update(id, updated_student.model_dump())
        return updated_student
