from typing import Callable, Awaitable, Any
from functools import wraps

from sqlalchemy import Engine, MetaData, Table
from sqlalchemy.exc import IntegrityError

from aioadmin.domain.exceptions import ForeignKeyConstraintError, TargetAlreadyExistsError
from aioadmin.domain.panel import Panel
from aioadmin.domain.table_data import TableDataGateway, TableSchema
from aioadmin.domain.row_data import Row


class SqlAlchemyTable(TableDataGateway):
    def __init__(self, engine: Engine, table: Table):
        self._engine: Engine = engine
        self._table: Table = table
        self._table_name: str = table.name

    def _get_session(func: Callable[..., Awaitable[Any]]):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            async with self._engine.connect() as session:
                self.session = session
                result = await func(self, *args, **kwargs)
                del self.session
                return result
        return wrapper

    @property
    def table_schema(self) -> TableSchema:
        return TableSchema(
            table_name=self._table_name,
            columns=list(self._table.columns.keys())
        )
    
    @_get_session
    async def find(self, column: str, value: str) -> Row | None:
        query = self._table.select().where(self._table.c[column] == value)
        result = await self.session.execute(query)
        row = result.fetchone()
        if row is not None:
            return Row(columns=self.table_schema.columns, values=row)
        else:
            return None
    
    @_get_session
    async def find_all(self) -> list[Row]:
        query = self._table.select()
        result = await self.session.execute(query)
        rows = result.fetchall()
        return [Row(columns=self.table_schema.columns, values=row) for row in rows]

    @_get_session
    async def save(self, data: dict) -> None:
        query = self._table.insert().values(**data)
        try:
            await self.session.execute(query)
        except IntegrityError:
            raise TargetAlreadyExistsError("Record already exists")
        await self.session.commit()
    
    @_get_session
    async def delete(self, column: str, value: str) -> None:
        query = self._table.delete().where(self._table.c[column] == value)
        try:
            await self.session.execute(query)
        except IntegrityError:
            raise ForeignKeyConstraintError("Cannot delete record due to foreign key constraint")
        await self.session.commit()


class SqlAlchemyConnection:
    def __init__(self, name: str, engine: Engine, metadata: MetaData):
        self._engine: Engine = engine
        self._metadata: MetaData = metadata
        self.panel: Panel = Panel(
            name=name,
            tables=[
                SqlAlchemyTable(engine=self._engine, table=table)
                for table in self._metadata.tables.values()
            ],
        )
    
