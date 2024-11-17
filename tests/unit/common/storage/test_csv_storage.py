import pytest
from src.common.storage.csv_storage import CSVStorageHandler


@pytest.fixture
def csv_storage_handler():
    handler = CSVStorageHandler("students_test.csv")
    yield handler
    open("students_test.csv", "w").close()  # Clears file after each test


class TestCSVStorageHandler:
    def test_save(self, csv_storage_handler):
        csv_storage_handler.save(
            {
                "id": 1,
                "name": "John",
                "surname": "Daw",
                "degree": "Bachelor",
                "semester": 4,
            }
        )
        assert csv_storage_handler.load() == [
            {
                "id": "1",
                "name": "John",
                "surname": "Daw",
                "degree": "Bachelor",
                "semester": "4",
            }
        ]

    def test_save_100_students(self, csv_storage_handler):
        for i in range(1, 101):
            csv_storage_handler.save(
                {
                    "id": i,
                    "name": f"John{i}",
                    "surname": f"Daw{i}",
                    "degree": "Bachelor",
                    "semester": 4,
                }
            )
        assert csv_storage_handler.load()[-1]["id"] == "100"
        assert csv_storage_handler.load()[0]["id"] == "1"
        assert len(csv_storage_handler.load()) == 100

    def test_save_existing_id(self, csv_storage_handler):
        csv_storage_handler.save(
            {
                "id": 1,
                "name": "John",
                "surname": "Daw",
                "degree": "Bachelor",
                "semester": 4,
            }
        )
        csv_storage_handler.save(
            {
                "id": 1,
                "name": "Jane",
                "surname": "Smith",
                "degree": "Bachelor",
                "semester": 6,
            }
        )
        assert csv_storage_handler.load() == [
            {
                "id": "1",
                "name": "John",
                "surname": "Daw",
                "degree": "Bachelor",
                "semester": "4",
            }
        ]

    def test_load_empty_file(self, csv_storage_handler):
        assert csv_storage_handler.load() == []

    def test_delete(self, csv_storage_handler):
        csv_storage_handler.save(
            {
                "id": 1,
                "name": "John",
                "surname": "Daw",
                "degree": "Bachelor",
                "semester": 4,
            }
        )
        csv_storage_handler.delete(1)
        assert csv_storage_handler.load() == []

    def test_delete_non_existing_id(self, csv_storage_handler):
        csv_storage_handler.delete(1)
        assert csv_storage_handler.load() == []

    def test_update(self, csv_storage_handler):
        csv_storage_handler.save(
            {
                "id": 1,
                "name": "John",
                "surname": "Daw",
                "degree": "Bachelor",
                "semester": 4,
            }
        )
        csv_storage_handler.update(
            1, {"name": "Jane", "surname": "Smith", "degree": "Bachelor", "semester": 6}
        )
        assert csv_storage_handler.load() == [
            {
                "id": "1",
                "name": "Jane",
                "surname": "Smith",
                "degree": "Bachelor",
                "semester": "6",
            }
        ]

    def test_update_non_existing_id(self, csv_storage_handler):
        csv_storage_handler.update(
            1, {"name": "Jane", "surname": "Smith", "degree": "Bachelor", "semester": 6}
        )
        assert csv_storage_handler.load() == []
