from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder
from redis.asyncio import Redis

from src.config.settings import Settings, settings
from src.keyboards.menu import get_subs_list_keyboard, get_specific_sub_keyboard, get_main_menu_keyboard
from src.services.backend_api import api_client
from src.services.naming import create_subscription_name_by_tg_id

router = Router()


@router.callback_query(lambda c: c.data == "my_subs_btn_click")
async def process_my_subs_btn_click(
        callback_query: types.CallbackQuery,
        redis: Redis
):
    try:
        builder = InlineKeyboardBuilder()

        subscriptions_info = await api_client.fetch_user_subscriptions(tg_id=callback_query.from_user.id)

        if subscriptions_info is None:
            await callback_query.message.edit_text(
                "Не удалось получить список.",
                reply_markup=get_main_menu_keyboard()
            )
            await callback_query.answer()
            return

        if not subscriptions_info:
            builder.row(types.InlineKeyboardButton(text="Создать новую подписку", callback_data="new_sub_1"))
            builder.row(types.InlineKeyboardButton(text="Назад в главное меню", callback_data="back_to_main"))

            await callback_query.message.edit_text(
                "У вас еще нет активных подписок.",
                reply_markup=builder.as_markup()
            )
            await callback_query.answer()
            return

        user_subs_info = "<b>📋 Список ваших VPN-подписок:</b>\n\n"
        for ind, sub in enumerate(subscriptions_info, start=1):
            status = "Работает" if sub.get("enable") else "Отключен"
            user_subs_info += f"{ind}. 🔑 <code>{sub.get('email')}</code>\n"
            user_subs_info += f"   └── Статус: {status} | Лимит: {"ꝏ" if sub.get('total_gb') == 0 else sub.get('total_gb')} GB\n\n"

            sub_id = sub.get("id")
            email = sub.get("email")

            await redis.delete(f"sub:{sub_id}")
            await redis.set(f"sub:{sub_id}", email, ex=1800)

        await callback_query.message.edit_text(
            text=user_subs_info,
            reply_markup=get_subs_list_keyboard(subscriptions_info)
        )
        await callback_query.answer()
    except TelegramBadRequest:
        await callback_query.answer()


@router.callback_query(F.data.startswith("view_sub_"))
async def process_view_specific_sub(callback_query: types.CallbackQuery):
    builder = InlineKeyboardBuilder()

    sub_id = callback_query.data.split("_")[-1]

    await callback_query.message.edit_text(
        text=f"Управление подпиской <b>ID: {sub_id}</b>",
        reply_markup=get_specific_sub_keyboard(sub_id)
    )

    builder.row(
        types.InlineKeyboardButton(
            text=f"Подписка #{1}",
            callback_data=f"view_sub_{sub_id}"
        )
    )

    await callback_query.answer()


@router.callback_query(F.data.startswith("copy_link_"))
async def process_view_specific_sub(
        callback_query: types.CallbackQuery,
        redis: Redis
):
    sub_id = callback_query.data.split("_")[-1]

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="⬅️ Назад к подписке",
            callback_data=f"view_sub_{sub_id}"
        )
    )

    client_email_from_redis = await redis.get(f"sub:{sub_id}")

    if not client_email_from_redis:
        await callback_query.message.answer(
            text="Произошла ошибка!"
        )
        return

    subscription_link = await api_client.fetch_subscription_link(
        email=client_email_from_redis
    )

    await callback_query.message.edit_text(
        text=f"Нажмите на текст ниже, чтобы скопировать ссылку:\n\n<code>{subscription_link}</code>",
        reply_markup=builder.as_markup()
    )

    await callback_query.answer()


@router.callback_query(F.data.startswith("delete_"))
async def process_view_specific_sub(
        callback_query: types.CallbackQuery,
        redis: Redis
):
    sub_id = callback_query.data.split("_")[-1]

    client_email_from_redis = await redis.get(f"sub:{sub_id}")

    if not client_email_from_redis:
        await callback_query.message.answer(
            text="Произошла ошибка!",
            reply_markup = get_main_menu_keyboard()
        )
        return

    await api_client.delete_subscription(
        email=client_email_from_redis
    )

    await callback_query.message.edit_text(
        text=f"Подписка успешно удалена!",
        reply_markup=get_main_menu_keyboard()
    )

    await redis.delete(f"sub:{sub_id}")

    await callback_query.answer()


@router.callback_query(F.data.startswith("new_sub_1"))
async def process_new_sub_btn_click_1(
        callback_query: types.CallbackQuery
):
    builder = InlineKeyboardBuilder()

    user_balance = await api_client.fetch_user_balance(
        tg_id=callback_query.from_user.id
    )

    if user_balance is None:
        await callback_query.message.edit_text(
            text=f"Нам не удалось получить Ваш баланс, повторите попытку позже.",
            reply_markup=get_main_menu_keyboard()
        )
        return

    if user_balance <= 0:
        await callback_query.message.edit_text(
            text=f"На данный момент Ваш баланс: <b>{user_balance}</b>.\n\n"
                 f"<b>Для приобретения подписки баланс должен быть больше 0.</b>",
            reply_markup=get_main_menu_keyboard()
        )
        return

    builder.row(
        types.InlineKeyboardButton(
            text="Создать новую подписку!",
            callback_data="new_sub_2"
        )
    )

    builder.row(
        types.InlineKeyboardButton(
            text="⬅️ Отмена, назад",
            callback_data="back_to_main"
        )
    )

    await callback_query.message.edit_text(
        text=f"Вы точно уверены?",
        reply_markup=builder.as_markup()
    )

    await callback_query.answer()


@router.callback_query(F.data.startswith("new_sub_2"))
async def process_new_sub_btn_click_1(
        callback_query: types.CallbackQuery
):
    tg_id = callback_query.from_user.id

    subscription_name = create_subscription_name_by_tg_id(
        tg_id=tg_id
    )

    response = await api_client.create_subscription(
        email=subscription_name,
        total_gb=0,
        expiry_time=0,
        tg_id=tg_id,
        limit_ip=settings.vpn.limit_ip,
        enable=True,
        inbounds=settings.vpn.inbounds
    )

    if response and response.get("success") == True:
        await callback_query.message.edit_text(
            text=f"Новая подписка успешно создана!",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await callback_query.message.edit_text(
            text=f"произшла ошибка при создании подписки.",
            reply_markup=get_main_menu_keyboard()
        )

    await callback_query.answer()

