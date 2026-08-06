import asyncio

from aiocryptopay import AioCryptoPay, Networks
from aiogram import Dispatcher
from redis.asyncio import Redis

from src.config.settings import settings
from src.handlers import main_router
from src.loader import bot, dp
from src.logs import setup_logging, logger
from src.rmq_client.consumer import start_consuming


CRYPTO_TOKEN = settings.crypto.token

_crypto_client = None

def get_crypto() -> AioCryptoPay:
    global _crypto_client
    if _crypto_client is None:
        _crypto_client = AioCryptoPay(token=CRYPTO_TOKEN, network=Networks.TEST_NET)
    return _crypto_client


async def on_startup(dispatcher: Dispatcher):
    dispatcher["consuming_task"] = asyncio.create_task(start_consuming())
    logger.info("RabbitMQ/Kafka consumer started")


async def on_shutdown(dispatcher: Dispatcher):
    logger.info("Stopping background tasks...")
    consuming_task = dispatcher.get("consuming_task")
    crypto_client: AioCryptoPay = dp.get("crypto")
    if crypto_client:
        await crypto_client.close()
        logger.info("CryptoPay session closed")
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
    crypto_client = AioCryptoPay(token=CRYPTO_TOKEN, network=Networks.TEST_NET)
    dp["redis"] = redis_pool
    dp["crypto"] = crypto_client
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    try:
        setup_logging()
        logger.info("Set up logging")
        logger.info(f"secret key: {settings.api_security.api_secret_key}") # TODO: убрать
        await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(bot)
    finally:
        await redis_pool.aclose()
        await bot.session.close()
        logger.info("Connections closed. Process finished.")



if __name__ == "__main__":
    print("Started TG-bot")
    asyncio.run(main())