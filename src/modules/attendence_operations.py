from src.common.storage.storage import StorageHandler
from src.common.models import AttendenceRecord, BaseAttendenceRecord
from typing import List
from pydantic import ValidationError
from datetime import datetime


class AttendenceDataError(Exception):
    """Exception raised for errors in attendence data."""

    pass


class AttendenceOperations:
    """Class for managing attendance operations.

    This class provides methods for CRUD operations on attendance records using a storage handler.
    """

    def __init__(self, storage_handler: StorageHandler):
        """Initialize AttendenceOperations with a storage handler.

        Args:
            storage_handler (StorageHandler): Handler for attendance data storage operations
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
        """
        attendence_records = self.__get_all_attendence_records()
        filtered_by_classroom_attendence_records = [
            record
            for record in attendence_records
            if record.classroom_id == classroom_id
        ]
        return filtered_by_classroom_attendence_records

    def get_attendence_records_by_student(
        self, student_id: int
    ) -> List[AttendenceRecord]:
        """Get list of attendance records for a specific student.

        Args:
            student_id (int): ID of the student to filter by

        Returns:
            List[AttendenceRecord]: List of attendance records for the student
        """
        attendence_records = self.__get_all_attendence_records()
        filtered_by_student_attendence_records = [
            record for record in attendence_records if record.student_id == student_id
        ]
        return filtered_by_student_attendence_records

    def get_attendence_records_by_date(self, date: datetime) -> List[AttendenceRecord]:
        """Get list of attendance records for a specific date.

        Args:
            date (datetime): Date to filter by

        Returns:
            List[AttendenceRecord]: List of attendance records for the date
        """
        attendence_records = self.__get_all_attendence_records()
        filtered_by_date_attendence_records = [
            record for record in attendence_records if record.date == date
        ]
        return filtered_by_date_attendence_records

    def __get_all_attendence_records(self) -> List[AttendenceRecord]:
        """Get list of all attendance records.

        Returns:
            List[AttendenceRecord]: List of all attendance records

        Raises:
            AttendenceDataError: When attendance record data is invalid
        """
        try:
            attendence_records = [
                AttendenceRecord(**attendence_record_data)
                for attendence_record_data in self.storage_handler.load()
            ]
        except ValidationError as e:
            raise AttendenceDataError(
                f"Invalid attendence record data format: {str(e)}"
            ) from e

        return attendence_records

    def add_attendence_record(
        self, attendence_record: BaseAttendenceRecord
    ) -> AttendenceRecord:
        """Add a new attendance record.

        Args:
            attendence_record (BaseAttendenceRecord): Attendance record data to add

        Returns:
            AttendenceRecord: The newly created attendance record with generated ID
        """
        attendence_record = AttendenceRecord(
            id=self.storage_handler.generate_id(), **attendence_record.model_dump()
        )
        self.storage_handler.save(attendence_record.model_dump())
        return attendence_record

    def delete_attendence_record(self, id: int):
        """Delete an attendance record by ID.

        Args:
            id (int): ID of the attendance record to delete
        """
        # TODO: Handle non-existing attendence record in delete
        self.storage_handler.delete(id)
