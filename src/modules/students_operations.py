from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.common.models import Student
from pydantic import ValidationError

class StorageHandler(ABC):
    
    @abstractmethod
    def save(self, data: Dict[str, Any]):
        pass

    @abstractmethod
    def load(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

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

        for student_data in students_data:
            try: 
                student = Student(**student_data)
                students.append(student)
            except ValidationError as e:
                raise StudentDataError(f"Invalid student data format: {str(e)}") from e

        return students
