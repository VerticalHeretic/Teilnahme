from datetime import datetime
from typing import Any, Dict, List

import pytest

from src.common.models import AttendenceRecord, BaseAttendenceRecord
from src.common.storage.storage import StorageHandler
from src.modules.attendence_operations import AttendenceDataError, AttendenceOperations


class MockAttendenceStorage(StorageHandler):
    def __init__(self, attendence_records: List[AttendenceRecord]):
        self.attendence_records = attendence_records

    def save(self, data: Dict[str, Any]):
        self.attendence_records.append(AttendenceRecord(**data))

    def load(self) -> List[Dict[str, Any]]:
        return [r.model_dump() for r in self.attendence_records]

    def delete(self, id: int):
        self.attendence_records = [r for r in self.attendence_records if r.id != id]

    def update(self, id: int, data: Dict[str, Any]):
        index = next(
            (
                index
                for index, record in enumerate(self.attendence_records)
                if record.id == id
            ),
            None,
        )

        if index is not None:
            self.attendence_records[index] = AttendenceRecord(**data)

    def generate_id(self) -> int:
        return len(self.attendence_records) + 1


class TestAttendenceOperations:
    def test_get_attendence_records_for_classroom(self):
        # Given
        attendence_record = AttendenceRecord(
            id=1, classroom_id=1, student_id=1, date=datetime.now()
        )
        attendence_record2 = AttendenceRecord(
            id=2, classroom_id=2, student_id=1, date=datetime.now()
        )
        attendence_storage = MockAttendenceStorage(
            [attendence_record, attendence_record2]
        )
        attendence_operations = AttendenceOperations(attendence_storage)
        want = [attendence_record]

        # When
        got = attendence_operations.get_attendence_records_by_classroom(1)

        # Then
        assert got == want

    def test_get_attendence_records_for_classroom_when_no_attendence_records(self):
        # Given
        attendence_storage = MockAttendenceStorage([])
        attendence_operations = AttendenceOperations(attendence_storage)
        want = []

        # When
        got = attendence_operations.get_attendence_records_by_classroom(1)

        # Then
        assert got == want

    def test_get_attendence_records_for_classroom_raises_error_when_invalid_attendence_record_data(
        self,
    ):
        # Given
        attendence_storage = MockAttendenceStorage(
            [
                BaseAttendenceRecord(
                    id=1, classroom_id=1, student_id=1, date=datetime.now()
                )
            ]
        )
        attendence_operations = AttendenceOperations(attendence_storage)

        # When
        with pytest.raises(AttendenceDataError):
            attendence_operations.get_attendence_records_by_classroom(1)

    def test_get_attendence_records_for_student_id(self):
        # Given
        attendence_record = AttendenceRecord(
            id=1, classroom_id=1, student_id=1, date=datetime.now()
        )
        attendence_record2 = AttendenceRecord(
            id=2, classroom_id=2, student_id=1, date=datetime.now()
        )
        attendence_storage = MockAttendenceStorage(
            [attendence_record, attendence_record2]
        )
        attendence_operations = AttendenceOperations(attendence_storage)
        want = [attendence_record, attendence_record2]

        # When
        got = attendence_operations.get_attendence_records_by_student(1)

        # Then
        assert got == want

    def test_get_attendence_records_for_date(self):
        # Given
        date1 = datetime(2024, 1, 1, 10, 0)
        date2 = datetime(2024, 1, 2, 10, 0)
        attendence_record = AttendenceRecord(
            id=1, classroom_id=1, student_id=1, date=date1
        )
        attendence_record2 = AttendenceRecord(
            id=2, classroom_id=2, student_id=1, date=date2
        )
        attendence_storage = MockAttendenceStorage(
            [attendence_record, attendence_record2]
        )
        attendence_operations = AttendenceOperations(attendence_storage)
        want = [attendence_record]

        # When
        got = attendence_operations.get_attendence_records_by_date(date1)

        # Then
        assert got == want

    def test_add_attendence_record(self):
        # Given
        attendence_record = BaseAttendenceRecord(
            classroom_id=1, student_id=1, date=datetime.now()
        )
        attendence_storage = MockAttendenceStorage([])
        attendence_operations = AttendenceOperations(attendence_storage)
        want = AttendenceRecord(id=1, **attendence_record.model_dump())

        # When
        got = attendence_operations.add_attendence_record(attendence_record)

        # Then
        assert got == want

    def test_add_attendence_record_id_is_generated(self):
        # Given
        attendence_record = BaseAttendenceRecord(
            classroom_id=1, student_id=1, date=datetime.now()
        )
        attendence_storage = MockAttendenceStorage([attendence_record])
        attendence_operations = AttendenceOperations(attendence_storage)
        want = AttendenceRecord(id=2, **attendence_record.model_dump())

        # When
        got = attendence_operations.add_attendence_record(attendence_record)

        # Then
        assert got == want

    def test_delete_attendence_record(self):
        # Given
        attendence_record = AttendenceRecord(
            id=1, classroom_id=1, student_id=1, date=datetime.now()
        )
        attendence_storage = MockAttendenceStorage([attendence_record])
        attendence_operations = AttendenceOperations(attendence_storage)
        want = []

        # When
        attendence_operations.delete_attendence_record(1)

        # Then
        assert attendence_storage.attendence_records == want
