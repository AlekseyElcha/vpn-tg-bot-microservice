import json

import aio_pika

from src.config.settings import settings
from src.logs import logger
from src.services.task_association import TASKS


async def get_rmq_connection():
    return await aio_pika.connect_robust(
        host=settings.rabbitmq.host,
        port=settings.rabbitmq.port,
        login=settings.rabbitmq.user,
        password=settings.rabbitmq.password,
    )


async def consume_messages(channel):
    queue = await channel.declare_queue("tasks", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    payload = json.loads(message.body.decode())
                    task_type = payload.get("action")

                    action = TASKS.get(task_type)
                    if action:
                        await action(payload)
                    else:
                        print(f"Неизвестный тип задачи: {task_type}")
                except Exception as e:
                    print(f"Ошибка обработки сообщения: {e}")


async def start_consuming():
    connection = await get_rmq_connection()

    async with connection.channel() as channel:
        await channel.set_qos(prefetch_count=1)
        await consume_messages(channel=channel)
        logger.info("RabbitMQ accepting messages.")
