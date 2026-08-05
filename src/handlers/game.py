from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from src.keyboards.menu import get_main_menu_keyboard
from src.services.backend_api import api_client

router = Router()

@router.callback_query(lambda c: c.data == "daily_challenge_btn_click")
async def process_daily_challenge_btn_click(c: CallbackQuery):
    try:
        user_tg_id = c.from_user.id

        server_response_msg = await api_client.register_check_in_daily_game(
            tg_id=user_tg_id
        )

        if ("Получена награда" in server_response_msg) or ("Поздравляем" in server_response_msg):
            await c.message.answer(
                text=f"<b>{server_response_msg}</b>",
                parse_mode="HTML",
                reply_markup=get_main_menu_keyboard(),
                message_effect_id="5046509860389126442"
            )
        else:
            await c.message.edit_text(
                text=server_response_msg,
                reply_markup=get_main_menu_keyboard(),
            )
        await c.answer()
    except TelegramBadRequest as e:
        if "message is not modified" in e.message:
            await c.answer()
        else:
            print(e.message)
            await c.answer("Произошла ошибка при обновлении экрана.")





