from datetime import datetime

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.common.models import AttendenceRecord
from src.common.storage.db_storage import DBStorageHandler
from src.modules.attendence_operations import AttendenceOperations


@pytest.fixture
def test_db():
    engine = create_engine(
        "sqlite://",  # In-memory SQLite database URL - creates temporary database that exists only during test execution
        connect_args={
            "check_same_thread": False
        },  # SQLite-specific setting that allows multiple threads to access the same connection
        poolclass=StaticPool,  # Uses a single connection for all operations - ideal for testing as it maintains consistent state
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestAttendenceOperations:
    def test_get_attendence_records_for_classroom(self, test_db):
        # Given
        attendence_records = [
            AttendenceRecord(id=1, classroom_id=1, student_id=1, date=datetime.now()),
            AttendenceRecord(id=2, classroom_id=2, student_id=1, date=datetime.now()),
        ]

        for record in attendence_records:
            test_db.add(record)
        test_db.commit()
        attendence_operations = AttendenceOperations(DBStorageHandler(test_db))

        # When
        got = attendence_operations.get_attendence_records_by_classroom(1)

        # Then
        assert got == [attendence_records[0]]

    def test_get_attendence_records_for_classroom_when_no_attendence_records(
        self, test_db
    ):
        # Given
        attendence_storage = DBStorageHandler(test_db)
        attendence_operations = AttendenceOperations(attendence_storage)
        want = []

        # When
        got = attendence_operations.get_attendence_records_by_classroom(1)

        # Then
        assert got == want

    def test_get_attendence_records_for_student_id(self, test_db):
        # Given
        attendence_records = [
            AttendenceRecord(id=1, classroom_id=1, student_id=1, date=datetime.now()),
            AttendenceRecord(id=2, classroom_id=2, student_id=1, date=datetime.now()),
        ]

        for record in attendence_records:
            test_db.add(record)
        test_db.commit()
        attendence_operations = AttendenceOperations(DBStorageHandler(test_db))
        want = attendence_records

        # When
        got = attendence_operations.get_attendence_records_by_student(1)

        # Then
        assert got == want

    def test_get_attendence_records_for_date(self, test_db):
        # Given
        date1 = datetime(2024, 1, 1, 10, 0)
        date2 = datetime(2024, 1, 2, 10, 0)
        attendence_records = [
            AttendenceRecord(id=1, classroom_id=1, student_id=1, date=date1),
            AttendenceRecord(id=2, classroom_id=2, student_id=1, date=date2),
        ]

        for record in attendence_records:
            test_db.add(record)
        test_db.commit()

        attendence_operations = AttendenceOperations(DBStorageHandler(test_db))
        want = attendence_records[0]

        # When
        got = attendence_operations.get_attendence_records_by_date(date1)

        # Then
        assert got == [want]

    def test_add_attendence_record(self, test_db):
        # Given
        attendence_record = AttendenceRecord(
            classroom_id=1, student_id=1, date=datetime.now()
        )
        test_db.add(attendence_record)
        test_db.commit()
        attendence_operations = AttendenceOperations(DBStorageHandler(test_db))

        # When
        got = attendence_operations.add_attendence_record(attendence_record)

        # Then
        assert got == attendence_record

    def test_delete_attendence_record(self, test_db):
        # Given
        attendence_record = AttendenceRecord(
            id=1, classroom_id=1, student_id=1, date=datetime.now()
        )
        test_db.add(attendence_record)
        test_db.commit()
        attendence_operations = AttendenceOperations(DBStorageHandler(test_db))

        # When
        attendence_operations.delete_attendence_record(1)

        # Then
        assert test_db.get(AttendenceRecord, 1) is None
