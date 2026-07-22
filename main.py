import asyncio

from redis.asyncio import Redis

from src.handlers import main_router
from src.loader import bot, dp


async def main():
    dp.include_router(main_router)

    redis_pool = Redis.from_url("redis://localhost:6379", decode_responses=True)

    dp["redis"] = redis_pool

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await redis_pool.aclose()
        await bot.session.close()


if __name__ == "__main__":
    print("Started TG-bot")
    asyncio.run(main())