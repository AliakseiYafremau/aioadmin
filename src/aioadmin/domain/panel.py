from aioadmin.domain.row_data import Row
from aioadmin.domain.table_data import TableDataGateway


class Panel:
    def __init__(self, name: str, tables: list[TableDataGateway]):
        self.name = name
        self.tables: dict[str, TableDataGateway] = {}
        for gateway in tables:
            self.tables[gateway.table_schema.table_name] = gateway

    def validate_table(self, table: str) -> bool:
        if table in self.tables:
            return True
        else:
            raise ValueError(f"Table '{table}' does not exist in panel '{self.name}'")

    async def find(self, table: str, column: str, value: str) -> Row | None:
        self.validate_table(table)
        return await self.tables[table].find(column, value)
    
    async def find_all(self, table: str) -> list[Row] | None:
        self.validate_table(table)
        return await self.tables[table].find_all()
    
    async def save(self, table: str, data: dict) -> None:
        self.validate_table(table)
        await self.tables[table].save(data)

    async def delete(self, table: str, column: str, value: str) -> None:
        self.validate_table(table)
        await self.tables[table].delete(column, value)