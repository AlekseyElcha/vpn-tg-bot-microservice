from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.settings import settings
from src.logs import logger
from src.services.backend_api import api_client


async def get_main_menu_keyboard(tg_id: int):
    builder = InlineKeyboardBuilder()
    user_valid_for_trial = await api_client.check_trial_validity(tg_id=tg_id)
    logger.info(user_valid_for_trial)

    builder.row(types.InlineKeyboardButton(text="Мои подписки 📋", callback_data="my_subs_btn_click"))
    builder.row(types.InlineKeyboardButton(text="Баланс 💳", callback_data="my_balance_btn_click"))
    builder.row(types.InlineKeyboardButton(text="Тарифы 🌟", callback_data="pricelist_btn_click"))
    builder.row(types.InlineKeyboardButton(text="Статус сервиса 📊", callback_data="service_status_btn_click"))
    builder.row(types.InlineKeyboardButton(text="Активировать промокод 💰", callback_data="promocode_btn_click"))
    builder.row(types.InlineKeyboardButton(text="Реферальная система 🤝", callback_data="referrals_btn_click"))
    builder.row(types.InlineKeyboardButton(text="Ежедневный челлендж 🎯", callback_data="daily_challenge_btn_click"))
    if user_valid_for_trial:
        builder.row(types.InlineKeyboardButton(text="Пробный период! 🎁", callback_data="trial_btn_click"))

    return builder.as_markup()


def get_main_admin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Написать пользователю", callback_data="direct_message_btn_click"))
    builder.row(types.InlineKeyboardButton(text="Массовая рассылка", callback_data="mass_message_btn_click"))
    builder.row(types.InlineKeyboardButton(text="Выйти из режима админа", callback_data="back_to_main"))
    return builder.as_markup()


def get_subs_list_keyboard(subscriptions: list):
    builder = InlineKeyboardBuilder()

    for i, sub in enumerate(subscriptions, start=1):
        sub_id = sub.get("id")
        is_enabled = "🟢" if sub.get("enable") else "🔴"

        builder.row(
            types.InlineKeyboardButton(
                text=f"{is_enabled} Подписка #{i}",
                callback_data=f"view_sub_{sub_id}"
            )
        )
    builder.row(types.InlineKeyboardButton(text="Создать новую подписку", callback_data="new_sub_1"))
    builder.row(types.InlineKeyboardButton(text="⬅️ В главное меню", callback_data="back_to_main"))
    return builder.as_markup()


def get_specific_sub_keyboard(sub_id: str):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🔗 Ссылка на подписку", callback_data=f"copy_link_{sub_id}"))
    builder.row(types.InlineKeyboardButton(text="📖 Более легкое подключение (Инструкции)", callback_data=f"instructions_{sub_id}"))
    builder.row(types.InlineKeyboardButton(text="❌ Удалить подписку", callback_data=f"delete_{sub_id}"))
    builder.row(types.InlineKeyboardButton(text="⬅️ К списку подписок", callback_data="my_subs_btn_click"))
    return builder.as_markup()

def get_platforms_keyboard(sub_id: str):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📱 Мобильные устройства", callback_data=f"plat_mobile_{sub_id}"))
    builder.row(types.InlineKeyboardButton(text="💻 Компьютеры (ПК)", callback_data=f"plat_pc_{sub_id}"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад к подписке", callback_data=f"view_sub_{sub_id}"))
    return builder.as_markup()

def get_mobile_os_keyboard(sub_id: str):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🍏 iOS (iPhone, iPad)", callback_data=f"os_ios_{sub_id}"))
    builder.row(types.InlineKeyboardButton(text="🤖 Android", callback_data=f"os_android_{sub_id}"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"instructions_{sub_id}"))
    return builder.as_markup()

def get_pc_os_keyboard(sub_id: str):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🪟 Windows", callback_data=f"os_windows_{sub_id}"))
    builder.row(types.InlineKeyboardButton(text="🍏 macOS", callback_data=f"os_mac_{sub_id}"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"instructions_{sub_id}"))
    return builder.as_markup()

def get_os_instruction_keyboard(sub_id: str, platform: str, web_link_url: str = None):
    builder = InlineKeyboardBuilder()
    if web_link_url:
        builder.row(types.InlineKeyboardButton(text="🚀 Перейти к настройке", url=web_link_url))
    back_btn_callback = f"plat_mobile_{sub_id}" if platform in ["ios", "android"] else f"plat_pc_{sub_id}"
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад к выбору ОС", callback_data=back_btn_callback))
    return builder.as_markup()


def get_balance_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"1 месяц - {settings.payment.price_1_month_rub} RUB 🇷🇺", callback_data="add_money_1_month_click"))
    builder.row(types.InlineKeyboardButton(text=f"3 месяца - {settings.payment.price_3_month_rub} RUB 🇷🇺", callback_data="add_money_3_month_click"))
    builder.row(types.InlineKeyboardButton(text=f"6 месяцев - {settings.payment.price_6_month_rub} RUB 🇷🇺", callback_data="add_money_6_month_click"))

    builder.row(types.InlineKeyboardButton(text="⬅️ В главное меню", callback_data="back_to_main"))
    return builder.as_markup()


# def get_specific_payment_keyboard():
#     builder = InlineKeyboardBuilder()
#     builder.row(types.InlineKeyboardButton(text="Telegram Stars", callback_data="add_stars"))
#     builder.row(types.InlineKeyboardButton(text="Crypto Bot", callback_data="add_crypto_bot"))
#     return builder.as_markup()


def get_promocode_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="⬅️ В главное меню", callback_data="back_to_main"))
    return builder.as_markup()


def get_referrals_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="⬅️ В главное меню", callback_data="back_to_main"))
    return builder.as_markup()
