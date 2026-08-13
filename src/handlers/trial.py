from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.settings import settings
from src.keyboards.menu import get_main_menu_keyboard
from src.services.backend_api import api_client
from src.services.naming import create_subscription_name_by_tg_id

router = Router()


@router.callback_query(lambda c: c.data == "trial_btn_click")
async def process_trial_btn_click(
        callback_query: CallbackQuery,
):
    builder = InlineKeyboardBuilder()
    user_tg_id = callback_query.from_user.id

    msg = (f"<b>Вам доступен бесплатный пробный период - 3 дня!</b>\n\n"
           f"Для начала использования УруруVPN Вам достаточно нажать на соответсвующую кнопку снизу!\n\n"
           f"Если Вы захотите продолжить пользоваться нашими услугами - достаточно будет просто пополнить баланс!")

    builder.row(types.InlineKeyboardButton(text="Подключить бесплатно на 3 дня", callback_data=f"start_trial_{user_tg_id}"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))

    await callback_query.message.edit_text(
        text=msg,
        reply_markup=builder.as_markup()
    )
    await callback_query.answer()


@router.callback_query(F.data.startswith("start_trial_"))
async def process_start_trial_btn(callback_query: CallbackQuery):
    user_tg_id = int(callback_query.data.split("start_trial_")[1])

    subscription_name = create_subscription_name_by_tg_id(
        tg_id=user_tg_id,
    )
    response = await api_client.create_subscription(
        email=subscription_name,
        total_gb=0,
        expiry_time=0,
        tg_id=user_tg_id,
        limit_ip=settings.vpn.limit_ip,
        enable=True,
        inbounds=settings.vpn.inbounds,
        is_trial=True
    )
    if response and response.get("success"):
        msg = (f"<b>Ваша пробная подписка успешно активирована!</b>\n\n"
           "Инструкции по подключению находятся в разделе «Мои подписки».")
    else:
        msg = "<b>Не удалось создать подписку. Повторите попытку позже!</b>"

    await callback_query.message.edit_text(
        text=msg,
        reply_markup=await get_main_menu_keyboard(user_tg_id)
    )
    await callback_query.answer()



