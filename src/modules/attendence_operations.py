from datetime import datetime
from typing import List

from src.common.errors import NotFoundError
from src.common.models import AttendenceRecord
from src.common.storage.storage import NewStorageHandler


class AttendenceDataError(Exception):
    """Exception raised for errors in attendence data."""

    pass


class AttendenceOperations:
    """Class for managing attendance operations.

    This class provides methods for CRUD (Create, Read, Update, Delete) operations on attendance records
    using a storage handler. It allows filtering records by classroom, student, and date.

    Attributes:
        storage_handler (NewStorageHandler): Handler for attendance data storage operations
    """

    def __init__(self, storage_handler: NewStorageHandler):
        """Initialize AttendenceOperations with a storage handler.

        Args:
            storage_handler (NewStorageHandler): Handler for attendance data storage operations
        """
        self.storage_handler = storage_handler

    def get_attendence_records_by_classroom(
        self, classroom_id: int
    ) -> List[AttendenceRecord]:
        """Get list of attendance records for a specific classroom.

        Args:
            classroom_id (int): ID of the classroom to filter by

        Returns:
            List[AttendenceRecord]: List of attendance records for the classroom

        Raises:
            NotFoundError: When classroom with given ID is not found
        """
        conditions = [AttendenceRecord.classroom_id == classroom_id]
        return self.storage_handler.get_all_where(AttendenceRecord, conditions)

    def get_attendence_records_by_student(
        self, student_id: int
    ) -> List[AttendenceRecord]:
        """Get list of attendance records for a specific student.

        Args:
            student_id (int): ID of the student to filter by

        Returns:
            List[AttendenceRecord]: List of attendance records for the student
        """
        conditions = [AttendenceRecord.student_id == student_id]
        return self.storage_handler.get_all_where(AttendenceRecord, conditions)

    def get_attendence_records_by_date(self, date: datetime) -> List[AttendenceRecord]:
        """Get list of attendance records for a specific date.

        Args:
            date (datetime): Date to filter by

        Returns:
            List[AttendenceRecord]: List of attendance records for the date
        """
        conditions = [AttendenceRecord.date == date]
        return self.storage_handler.get_all_where(AttendenceRecord, conditions)

    def add_attendence_record(
        self, attendence_record: AttendenceRecord
    ) -> AttendenceRecord:
        """Add a new attendance record.

        Args:
            attendence_record (AttendenceRecord): Attendance record data to add

        Returns:
            AttendenceRecord: The newly created attendance record with generated ID

        Raises:
            AttendenceDataError: If the attendance record data is invalid
        """
        return self.storage_handler.create(attendence_record)

    def delete_attendence_record(self, id: int):
        """Delete an attendance record by ID.

        Args:
            id (int): ID of the attendance record to delete

        Raises:
            NotFoundError: When attendance record with given ID is not found
        """
        try:
            self.storage_handler.delete(id, AttendenceRecord)
        except ValueError:
            raise NotFoundError(f"Attendence record with ID {id} not found")
