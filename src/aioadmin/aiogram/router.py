from aiogram import Router

from aioadmin.orm.sqlalchemy import SqlAlchemyConnection
from aioadmin.aiogram.middleware import ConnectionMiddleware
from aioadmin.aiogram.handlers.menu import menu_dialog


class AdminRouter(Router):
    def __init__(self, *, name = None, connection: SqlAlchemyConnection):
        super().__init__(name=name)
        middleware = ConnectionMiddleware(connection=connection)
        self.message.middleware.register(middleware=middleware)
        self.callback_query.middleware.register(middleware=middleware)
        self.include_routers(
            menu_dialog,
        )