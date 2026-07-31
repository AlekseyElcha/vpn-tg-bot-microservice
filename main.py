import asyncio

from aiogram import Dispatcher
from redis.asyncio import Redis

from src.handlers import main_router
from src.loader import bot, dp
from src.logs import setup_logging, logger
from src.rmq_client.consumer import start_consuming


async def on_startup(dispatcher: Dispatcher):
    dispatcher["consuming_task"] = asyncio.create_task(start_consuming())
    logger.info("RabbitMQ/Kafka consumer started")


async def on_shutdown(dispatcher: Dispatcher):
    logger.info("Stopping background tasks...")
    consuming_task = dispatcher.get("consuming_task")
    if consuming_task and not consuming_task.done():
        consuming_task.cancel()
        try:
            await consuming_task
        except asyncio.CancelledError:
            pass
    logger.info("Background tasks stopped")


async def main():
    dp.include_router(main_router)
    redis_pool = Redis.from_url("redis://localhost:6379", decode_responses=True)
    dp["redis"] = redis_pool

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    try:
        setup_logging()
        logger.info("Set up logging")
        await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(bot)
    finally:
        await redis_pool.aclose()
        await bot.session.close()
        logger.info("Connections closed. Process finished.")



if __name__ == "__main__":
    print("Started TG-bot")
    asyncio.run(main())