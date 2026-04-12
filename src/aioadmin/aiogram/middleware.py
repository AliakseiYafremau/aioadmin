from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from aioadmin.orm.sqlalchemy import SqlAlchemyConnection

class ConnectionMiddleware(BaseMiddleware):
    def __init__(self, connection: SqlAlchemyConnection):
        self.connection = connection
        self.panel = connection.panel

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        data['panel'] = self.panel
        return await handler(event, data)