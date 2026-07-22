from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Мои подписки 📋", callback_data="my_subs_btn_click"))
    builder.row(types.InlineKeyboardButton(text="Баланс 💳", callback_data="my_balance_btn_click"))
    builder.row(types.InlineKeyboardButton(text="Тарифы 🌟", callback_data="pricelist_btn_click"))
    builder.row(types.InlineKeyboardButton(text="Статус сервиса 📊", callback_data="service_status_btn_click"))
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
    builder.row(types.InlineKeyboardButton(text="Скопировать ссылку на подписку", callback_data=f"copy_link_{sub_id}"))
    builder.row(types.InlineKeyboardButton(text="Удалить подписку", callback_data=f"delete_{sub_id}"))
    builder.row(types.InlineKeyboardButton(text="⬅️ К списку подписок", callback_data="my_subs_btn_click"))
    return builder.as_markup()


def get_balance_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Пополнить баланс", callback_data="add_money_btn_click"))
    builder.row(types.InlineKeyboardButton(text="⬅️ В главное menu", callback_data="back_to_main"))
    return builder.as_markup()

