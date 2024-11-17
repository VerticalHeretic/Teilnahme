import csv
from typing import Any, Dict, List

from src.common.storage.storage import StorageHandler


class CSVStorageHandler(StorageHandler):
    """A storage handler implementation that uses CSV files to store data.

    This class implements the StorageHandler interface to provide CRUD operations
    using CSV files as the storage medium.
    """

    def __init__(self, file_path: str):
        """Initialize the CSV storage handler.

        Args:
            file_path: Path to the CSV file that will be used for storage
        """
        self.file_path = file_path

    def save(self, data: Dict[str, Any]):
        """Save new data to the CSV file.

        Args:
            data: Dictionary containing the data to save. Must include an 'id' field.

        If an entry with the same id already exists, the operation is skipped.
        """
        try:
            existing_data = self.load()
        except FileNotFoundError:
            existing_data = []

        if data.get("id") in [int(row.get("id")) for row in existing_data]:
            # TODO: Log that is exists already :)
            return

        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())

            # Check if file is empty by checking if cursor is at start (position 0)
            # If empty, write the CSV header row with the field names
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(data)

    def load(self) -> List[Dict[str, Any]]:
        """Load all data from the CSV file.

        Returns:
            List of dictionaries containing the data from each row in the CSV file.
        """
        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def delete(self, id: int):
        """Delete an entry from the CSV file.

        Args:
            id: The ID of the entry to delete.

        If the file is empty or the ID is not found, no action is taken.
        """
        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        if len(rows) == 0:
            # TODO: Log that the file is empty or something :)
            return

        with open(self.file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()

            [writer.writerow(row) for row in rows if int(row.get("id")) != id]

    def update(self, id: int, data: Dict[str, Any]):
        """Update an existing entry in the CSV file.

        Args:
            id: The ID of the entry to update
            data: Dictionary containing the new data for the entry
        """
        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        if len(rows) == 0:
            # TODO: Log that the file is empty or something :)
            return

        [row.update(data) for row in rows if int(row.get("id")) == id]

        with open(self.file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    def generate_id(self) -> int:
        """Generate a new ID for a new entry.

        Returns:
            int: The new ID
        """
        if len(self.load()) == 0:
            return 1

        return int(self.load()[-1]["id"]) + 1
