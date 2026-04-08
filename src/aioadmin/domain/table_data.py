from abc import ABC, abstractmethod

from aioadmin.domain.row_data import Row


class TableSchema:
    def __init__(self, table_name: str, columns: list[str]):
        self.table_name = table_name
        self.columns = columns


class TableDataGateway(ABC):
    @property
    @abstractmethod
    def table_schema(self) -> TableSchema:
        raise NotImplementedError


    @abstractmethod
    async def find(self, column: str, value: str) -> Row | None:
        raise NotImplementedError
    
    @abstractmethod
    async def find_all(self) -> list[Row]:
        raise NotImplementedError
    
    @abstractmethod
    async def save(self, data: dict) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, column: str, value: str) -> None:
        raise NotImplementedError