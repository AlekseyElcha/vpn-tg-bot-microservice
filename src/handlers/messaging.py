from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.keyboards.menu import get_main_admin_keyboard
from src.loader import bot

router = Router()

class DirectMessageStates(StatesGroup):
    wait_for_user_id = State()
    wait_for_message = State()

@router.callback_query(lambda c: c.data == "direct_message_btn_click")
async def send_direct_message_to_user_1(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()

    await callback_query.message.answer("Введите Telegram ID пользователя:")

    await state.set_state(DirectMessageStates.wait_for_user_id)


@router.message(DirectMessageStates.wait_for_user_id)
async def process_get_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ ID должен состоять только из цифр! Попробуйте снова:")

    user_id = int(message.text)
    await state.update_data(target_user_id=user_id)

    await message.answer(f"Введите текст сообщения:")

    await state.set_state(DirectMessageStates.wait_for_message)


@router.message(DirectMessageStates.wait_for_message)
async def process_get_message(message: types.Message, state: FSMContext):
    text_message = message.text
    data = await state.get_data()
    user_id = data.get("target_user_id")

    await bot.send_message(user_id, text_message)

    await state.clear()

    await message.answer(
        f"Сообщение отправлено пользователю {user_id}!",
        reply_markup=get_main_admin_keyboard()
    )

