from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import async_session_factory


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        async with async_session_factory() as session:
            data["session"] = session

            return await handler(event, data)