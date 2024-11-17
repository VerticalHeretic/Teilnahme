from abc import ABC, abstractmethod
from typing import Dict, Any, List, TypeVar
from pydantic import BaseModel
from sqlmodel import SQLModel

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

    @abstractmethod
    def update(self, id: int, data: Dict[str, Any]):
        pass

    @abstractmethod
    def generate_id(self) -> int:
        pass


# NewStorageHandler is a a new more generic storage handler interface, to make use of databases
# and other types of storage backends.
class NewStorageHandler(ABC):

    @abstractmethod
    def get_all(self) -> List[SQLModel]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> SQLModel:
        pass

    @abstractmethod
    def create(self, model: SQLModel) -> SQLModel:
        pass

    @abstractmethod
    def update(self, id: int, model: SQLModel) -> SQLModel:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass