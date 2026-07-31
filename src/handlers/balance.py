from aiogram import Router, types, F, Bot
from aiogram.client import bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from redis.asyncio import Redis

from pricelist import PaymentsPricesInfo
from src.keyboards.menu import get_balance_keyboard
from src.services.backend_api import api_client
from src.services.payment_link_creator import create_payment_link, PaymentData

router = Router()

# @router.callback_query(lambda c: c.data == "by_balance_btn_click")
# async def process_balance_menu(callback_query: types.CallbackQuery):
#     await callback_query.message.edit_text(
#         text="Вы перешли в баланс. Выберите действие:",
#         reply_markup=get_balance_keyboard()
#     )
#     await callback_query.answer()


@router.callback_query(lambda c: c.data == "my_balance_btn_click")
async def process_my_subs_btn_click(
        callback_query: types.CallbackQuery,
        # redis: Redis
):
    user_balance = await api_client.fetch_user_balance(
        tg_id=callback_query.from_user.id
    )

    # await redis.delete(f"balance:{callback_query.from_user.id}", user_balance)
    # await redis.set(f"balance:{callback_query.from_user.id}", user_balance)

    if user_balance is None:
        await callback_query.message.edit_text(
            text=f"Не удалось получить информацию о балансе.",
            reply_markup=get_balance_keyboard()
        )
    else:
        await callback_query.message.edit_text(
            text=f"Ваш баланс: {user_balance}",
            reply_markup=get_balance_keyboard()
        )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "add_money_btn_click")
async def process_add_money_btn_click(
        callback_query: types.CallbackQuery
):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text=f"60 Stars 🌟",
            callback_data=f"pay_Оплата услуг - 60 stars_btn_click"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=f"120 Stars 🌟",
            callback_data=f"pay_Оплата услуг - 120 stars_btn_click"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=f"240 Stars 🌟",
            callback_data=f"pay_Оплата услуг - 240 stars_btn_click"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=f"⬅️ Назад",
            callback_data=f"my_balance_btn_click"
        )
    )

    await callback_query.message.edit_text(
        text=f"Выберите сумму для пополнения:",
        reply_markup=builder.as_markup()
    )

    await callback_query.answer()


@router.callback_query(F.data.startswith("pay_"))
async def process_add_money_btn_click(
        callback_query: types.CallbackQuery
):
    builder = InlineKeyboardBuilder()

    tariff_name = callback_query.data.split("_")[1]

    stars_amount = PaymentsPricesInfo.associate_tariff_name_and_price(
        tariff_name=tariff_name
    )

    if not stars_amount:
        return

    payment_data = await create_payment_link(
        PaymentData(
            user_id=int(callback_query.from_user.id),
            item_id=tariff_name,
            price_stars=stars_amount
        )
    )

    if not payment_data:
        return

    payment_url = payment_data.get("pay_url")

    payment_text_for_user = (
        f"Ссылка для пополнения Вашего баланса на {stars_amount}🌟:\n\n\n"
        f"{payment_url}\n\n"
        f"Для проведения оплаты нажмите на ссылку и подтвердите операцию."
    )

    await callback_query.message.edit_text(
        text=payment_text_for_user,
        reply_markup=builder.as_markup()
    )


    await callback_query.answer()

@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(
        message: types.Message,
        bot: Bot,
):
    payment = message.successful_payment
    if not payment:
        return

    payload = payment.invoice_payload

    try:
        _, user_id, item_id = payload.split(":")
        user_id = int(user_id)
    except (ValueError, TypeError):
        return
    current_bot = message.bot

    await current_bot.send_message(
        chat_id=user_id,
        text=f"Оплата {payment.total_amount} 🌟 получена! \n\nВыполняем необходимые действия на сервере..."
    )

    server_response = await api_client.fetch_server_post_payment_task_result(
        user_id=user_id,
        item_id=item_id,
        payment_amount=payment.total_amount
    )

    if server_response is None:
        await bot.refund_star_payment(
            user_id=int(user_id),
            telegram_payment_charge_id=payment.telegram_payment_charge_id,
        )
        await bot.send_message(
            chat_id=int(user_id),
            text="Что-то пошло не так, поэтому мы вернули Ваши средства.",
            reply_markup=get_balance_keyboard()
        )

    server_task_successful = server_response.get("success")

    if not server_task_successful or server_task_successful == False:
        await bot.refund_star_payment(
            user_id=int(user_id),
            telegram_payment_charge_id=payment.telegram_payment_charge_id,
        )
        await bot.send_message(
            chat_id=int(user_id),
            text="Произошла ошибка, поэтому мы вернули Ваши средства.",
            reply_markup=get_balance_keyboard()
        )

    payment_test_mode_enabled = True
    if payment_test_mode_enabled:
        try:
            await bot.refund_star_payment(
                user_id=int(user_id),
                telegram_payment_charge_id=payment.telegram_payment_charge_id,
            )
            await bot.send_message(
                chat_id=int(user_id),
                text=f"<b>Ура! 🎉\n\n"
                     f"На баланс Вашего аккаунта успешно зачислено: {payment.total_amount}🌟\n\n"
                     f"Благодарим за пользование услугами УруруVPN!</b>\n\n"
                     f"тестовый режим вкл.- звёзды возвращены!",
                reply_markup=get_balance_keyboard(),
                message_effect_id="5046509860389126442"
            )
        except Exception as e:
            print(f"Не удалось выполнить автовозврат: {e}")
    else:
        await bot.send_message(
            chat_id=int(user_id),
            text=f"<b>Ура! 🎉\n\n"
                 f"На баланс Вашего аккаунта успешно зачислено {payment.total_amount}🌟\n\n"
                 f"Благодарим за пользование услугами УруруVPN!</b>",
            reply_markup=get_balance_keyboard(),
            message_effect_id="5046509860389126442"
        )
