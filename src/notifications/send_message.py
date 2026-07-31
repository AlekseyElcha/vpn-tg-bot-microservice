from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError, TelegramAPIError

from src.loader import bot


async def send_message_to_user(
        data: dict
):
    tg_id = data.get("tg_id")
    message = data.get("message")
    try:
        await bot.send_message(
            chat_id=tg_id,
            text=message
        )
    except TelegramBadRequest:
        print(1)
    except TelegramForbiddenError:
        print(2)
    except TelegramAPIError:
        print(3)
