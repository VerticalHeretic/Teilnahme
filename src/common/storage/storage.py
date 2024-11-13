from abc import ABC, abstractmethod
from typing import Dict, Any, List

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