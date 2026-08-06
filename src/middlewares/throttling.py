from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from redis.asyncio import Redis

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, rate_limit: float = 1.0):
        self.redis = redis
        self.rate_limit = rate_limit  # Разрешаем 1 действие в секунду

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            
        if user_id:
            key = f"throttle:{user_id}"
            is_allowed = await self.redis.set(key, "1", nx=True, ex=int(self.rate_limit))
            
            if not is_allowed:
                if isinstance(event, CallbackQuery):
                    await event.answer("Пожалуйста, не нажимайте кнопки так быстро ⏳", show_alert=False)
                return
                
        return await handler(event, data)