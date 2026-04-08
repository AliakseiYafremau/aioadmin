from aioadmin.orm.sqlalchemy import SqlAlchemyConnection, SqlAlchemyTable

from models import Base


async def test_connection_creates_panel_from_metadata(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    connection = SqlAlchemyConnection(name="admin", engine=engine, metadata=Base.metadata)

    assert connection.panel.name == "admin"
    assert tuple(connection.panel.tables) == ("tasks",)
    assert isinstance(connection.panel.tables["tasks"], SqlAlchemyTable)
    assert connection.panel.tables["tasks"].table_schema.table_name == "tasks"
    assert connection.panel.tables["tasks"].table_schema.columns == ["id", "description", "text"]


async def test_connection_panel_performs_crud_operations(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    connection = SqlAlchemyConnection(name="admin", engine=engine, metadata=Base.metadata)

    await connection.panel.save(
        table="tasks",
        data={"description": "first description", "text": "first text"},
    )
    await connection.panel.save(
        table="tasks",
        data={"description": "second description", "text": "second text"},
    )

    rows = await connection.panel.find_all("tasks")
    first_row = rows[0]
    second_row = rows[1]

    assert len(rows) == 2
    assert first_row.columns == ("id", "description", "text")
    assert first_row.values[1:] == ["first description", "first text"]
    assert second_row.values[1:] == ["second description", "second text"]

    first_id = first_row.values[0]
    row = await connection.panel.find("tasks", "id", first_id)

    assert row is not None
    assert row.values[0] == first_row.values[0]

    await connection.panel.delete("tasks", "id", first_id)

    assert await connection.panel.find_all("tasks") == [second_row]