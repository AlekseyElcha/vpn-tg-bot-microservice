import json

import aio_pika
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.settings import settings
from src.keyboards.menu import get_main_admin_keyboard
from src.loader import bot
from src.services.backend_api import api_client

router = Router()

class DirectMessageStates(StatesGroup):
    wait_for_user_id = State()
    wait_for_message = State()


class MassMessageStates(StatesGroup):
    wait_for_mass_message = State()


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


@router.callback_query(lambda c: c.data == "mass_message_btn_click")
async def send_direct_message_to_user_1(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()

    await callback_query.message.answer("Введите сообщение для рассылки всем пользователям:")

    await state.set_state(MassMessageStates.wait_for_mass_message)


@router.message(MassMessageStates.wait_for_mass_message)
async def process_get_id(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()

    message_for_users = message.text
    await state.update_data(message_for_users=message_for_users)

    builder.row(
        types.InlineKeyboardButton(
            text="Отправить!",
            callback_data="send_mass_message"
        )
    )

    builder.row(
        types.InlineKeyboardButton(
            text="⬅️ Отмена, назад",
            callback_data="back_to_main"
        )
    )

    await message.answer(
        text=f"<b>Отправить рассылку всем пользователям?</b>",
        reply_markup=builder.as_markup()
    )


@router.callback_query(lambda c: c.data == "send_mass_message")
async def process_get_id(message: types.Message, state: FSMContext):
    all_users_ids = await api_client.fetch_all_user_tg_ids()

    message_for_users = await state.get_data()

    rabbitmq_conn = await aio_pika.connect(settings.rabbitmq.rmq_connection_url)

    async with rabbitmq_conn, rabbitmq_conn.channel() as rmq_channel:
        for ind in range(len(all_users_ids)):
            payload = {
                "action": "notify",
                "tg_id": all_users_ids[ind],
                "message": f"[Сообщение от администратора] {message_for_users.get("message_for_users")}"
            }

            await rmq_channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(payload).encode("utf-8"),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key="notification_tasks"
            )

    await message.answer(
        f"Сообщения успешно отправлены!",
        reply_markup=get_main_admin_keyboard()
    )

    await state.clear()

