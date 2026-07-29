from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.keyboards.menu import get_promocode_keyboard, get_main_menu_keyboard
from src.loader import bot
from src.services.backend_api import api_client

router = Router()

class PromocodeStates(StatesGroup):
    wait_for_promocode = State()

@router.callback_query(lambda c: c.data == "promocode_btn_click")
async def process_promocode_btn_click(
        callback_query: types.CallbackQuery,
        state: FSMContext
):
    text = ("Промокоды УруруVPN дают бонусный баланс!\n\n"
            "Ищите их в нашем канале!\n\n"
            "Введите промокод для активации:")
    try:
        await callback_query.message.edit_text(
            text=text,
            reply_markup=get_promocode_keyboard()
        )
        await state.set_state(PromocodeStates.wait_for_promocode)
        await callback_query.answer()
    except TelegramBadRequest:
        await callback_query.answer()


@router.message(PromocodeStates.wait_for_promocode)
async def process_entered_promocode(message: types.Message, state: FSMContext):
    user_promocode = message.text.strip()

    response = await api_client.activate_bonus_code(
        code=user_promocode,
        tg_id=message.from_user.id
    )

    if response and response.get("success") and response.get("msg"):
        success_message = (f"Ура! Промокод активирован!"
                           f"{response.get("msg")}")
        await bot.send_message(message.chat.id,
                               success_message,
                               reply_markup=get_main_menu_keyboard(),
                               message_effect_id="5046509860389126442"
        )
    else:
        await bot.send_message(message.chat.id,
                               "Промокод не найден или устарел.",
                               reply_markup=get_main_menu_keyboard()
        )

        await state.clear()
