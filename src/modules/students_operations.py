from typing import List
from src.common.models import BaseStudent, Student
from src.common.storage.storage import StorageHandler
from pydantic import ValidationError

class StudentDataError(Exception):
    """Raises when student data is invalid"""
    pass

class StudentsOperations:
    def __init__(self, storage_handler: StorageHandler): 
        self.storage_handler = storage_handler

    def get_students(self) -> List[Student]:
        """Get list of all students
        
        Returns:
            List[Student]: List of students

        Raises: 
            StudentDataError: When student data is invalid
        """

        students_data = self.storage_handler.load()
        students = []

        try:
            students = [Student(**student_data) for student_data in students_data]
        except ValidationError as e:
            raise StudentDataError(f"Invalid student data format: {str(e)}") from e

        return students

    def add_student(self, student: BaseStudent):
        # TODO: Will need to check if the student is valid (i.e. if the degree is valid, if the semester is valid, etc.)
        # TODO: Will need to make the function async save

        """Add student to storage
        
        Args:
            student (Student): Student to add
        """
        student = Student(id=self.storage_handler.generate_id(), **student.model_dump())
        self.storage_handler.save(student.model_dump())

    def delete_student(self, id: int):
        """Delete student from storage
        
        Args:
            id (int): Student id
        """
        self.storage_handler.delete(id)

    def update_student(self, id: int, updated_student: Student):
        """Update student in storage
        
        Args:
            id (int): Student id
            updated_student (Student): Updated student data
        """
        self.storage_handler.update(id, updated_student.model_dump())
