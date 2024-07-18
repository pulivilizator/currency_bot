from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from bot.src.data_stores import Cache, CacheKeys


class CacheMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)
        cache: Cache = data['cache']
        user_id = user.id
        if not await cache.user_exists(user_id):
            await cache.set_user_data(user_id=user_id,
                                 key=CacheKeys.Settings.language(),
                                 value=user.language_code)

        return await handler(event, data)
