import csv
from typing import Dict, Any, List
from src.common.storage.storage import StorageHandler

class CSVStorageHandler(StorageHandler):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, data: Dict[str, Any]):
        existing_data = self.load()

        if data.get('id') in [int(row.get('id')) for row in existing_data]:
            # TODO: Log that is exists already :)
            return

        with open(self.file_path, mode="a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())         

            # Check if file is empty by checking if cursor is at start (position 0)
            # If empty, write the CSV header row with the field names
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(data)
    
    def load(self) -> List[Dict[str, Any]]:
        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def delete(self, id: int):
        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        if len(rows) == 0:
            return

        with open(self.file_path, mode="w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()

            [writer.writerow(row) for row in rows if int(row.get('id')) != id]

    def update(self, id: int, data: Dict[str, Any]):
        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        [row.update(data) for row in rows if int(row.get('id')) == id]
        
        with open(self.file_path, mode="w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writeheader()
            writer.writerows(rows)
