from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram import types

class DbPoolMiddleware(BaseMiddleware):
    """
    Middleware для передачи пула соединений asyncpg в обработчики через data['dp_pool'].
    """
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def __call__(self, handler, event: types.Update, data: dict):
        data['dp_pool'] = self.pool
        return await handler(event, data)
