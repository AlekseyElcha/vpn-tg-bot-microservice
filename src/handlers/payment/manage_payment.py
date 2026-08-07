from aiocryptopay import AioCryptoPay
from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config.settings import settings
from src.keyboards.menu import get_balance_keyboard, get_main_menu_keyboard
from src.loader import bot
from src.logs import logger
from src.services.backend_api import api_client
from src.services.payment_link_creator import create_payment_link, PaymentData

router = Router()

@router.callback_query(F.data.startswith("add_money_"))
async def process_add_money_btn_click(callback_query: types.CallbackQuery):
    builder = InlineKeyboardBuilder()

    month_count = int(callback_query.data.split("_")[2])

    builder.row(
        types.InlineKeyboardButton(
            text=f"Оплатить через CryptoBot 💸",
            callback_data=f"pay_crypto_{month_count}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=f"Оплатить Telegram Stars 🌟",
            callback_data=f"pay_stars_{month_count}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=f"⬅️ Назад",
            callback_data=f"my_balance_btn_click"
        )
    )

    await callback_query.message.edit_text(
        text=f"<b>Выберите удобный для Вас вариант оплаты:</b>",
        reply_markup=builder.as_markup()
    )
    await callback_query.answer()



@router.callback_query(F.data.startswith("pay_crypto_"), StateFilter("*"))
async def process_pay_crypto_btn_click(
        callback_query: types.CallbackQuery,
        crypto: AioCryptoPay
):
    month_count = int(callback_query.data.split("_")[-1])

    match month_count:
        case 1:
            amount = settings.payment.price_1_month_rub
        case 3:
            amount = settings.payment.price_3_month_rub
        case 6:
            amount = settings.payment.price_6_month_rub
        case _:
            amount = settings.payment.price_1_month_rub
            logger.warning("Unknown month count in process_pay_crypto_btn_click function: %s", month_count)

    payment_invoice = await crypto.create_invoice(
        currency_type="fiat",
        fiat="RUB",
        amount=amount,
        accepted_assets=["TON", "USDT"],
        description=f'Оплата подписки',
        payload=str(month_count)
    )

    pay_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 Оплатить в CryptoBot", url=payment_invoice.bot_invoice_url)],
        [InlineKeyboardButton(text="🔄 Проверить оплату", callback_data=f"check_{payment_invoice.invoice_id}")],
        [InlineKeyboardButton(text="⬅️ Вернуться в главное меню", callback_data=f"back_to_main")]
    ])

    await callback_query.message.answer(
        f"Счет успешно сгенерирован!\n"
        f"Сумма: <b>{payment_invoice.amount} RUB</b>\n\n"
        f"После оплаты <b>обязательно</b> нажмите кнопку <b>«Проверить оплату»</b> ниже.",
        reply_markup=pay_kb,
        parse_mode="HTML"
    )

    await callback_query.answer()


@router.callback_query(F.data.startswith("pay_stars_"), StateFilter("*"))
async def process_pay_stars_btn_click(
        callback_query: types.CallbackQuery
):
    builder = InlineKeyboardBuilder()

    month_count = int(callback_query.data.split("_")[-1])

    match month_count:
        case 1:
            amount = settings.payment.price_1_month_stars
        case 3:
            amount = settings.payment.price_3_month_stars
        case 6:
            amount = settings.payment.price_6_month_stars
        case _:
            amount = settings.payment.price_1_month_stars
            logger.warning("Unknown month count in process_pay_stars_btn_click function: %s", month_count)

    tariff_name = f"Оплата услуг {month_count} месяцев за звёзды"

    payment_data = await create_payment_link(
        PaymentData(
            user_id=int(callback_query.from_user.id),
            item_id=tariff_name,
            price_stars=amount,
            payload=str(month_count),
        )
    )

    if not payment_data:
        return

    payment_url = payment_data.get("pay_url")

    payment_text_for_user = (
        f"Ссылка для пополнения Вашего баланса на {amount}🌟:\n\n\n"
        f"{payment_url}\n\n"
        f"Для проведения оплаты нажмите на ссылку и подтвердите операцию."
    )

    builder.row(
        types.InlineKeyboardButton(
            text="⬅️ Вернуться в главное меню",
            callback_data="back_to_main"
        )
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
    """Обрабатывает успешную оплату звёздами тг"""
    payment = message.successful_payment
    if not payment:
        return

    payload = payment.invoice_payload

    try:
        month_count = int(payload)
    except (ValueError, TypeError):
        month_count = 1

    user_id = message.from_user.id
    stars_amount = payment.total_amount

    current_bot = message.bot

    await current_bot.send_message(
        chat_id=user_id,
        text=f"Оплата {payment.total_amount} 🌟 получена! \n\nВыполняем необходимые действия на сервере..."
    )

    server_response = await api_client.fetch_server_post_payment_task_result(
        user_id=user_id,
        item_id=f"{month_count} month",
        payment_amount=stars_amount,
        payment_type="Stars"
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


@router.callback_query(F.data.startswith("check_"))
async def check_payment_status(
        callback_query: types.CallbackQuery,
        crypto: AioCryptoPay
):
    """Проверяет оплату за криптовалюту"""
    invoice_id = int(callback_query.data.split("_")[1])

    invoices = await crypto.get_invoices(invoice_ids=invoice_id)

    if not invoices:
        await callback_query.answer("Счет не найден.", show_alert=True)
        return

    invoice = invoices[0] if isinstance(invoices, list) else invoices


    if invoice.status == 'paid':
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer("🎉 Оплата прошла успешно!", show_alert=True)

        server_response = await api_client.fetch_server_post_payment_task_result(
                        user_id=callback_query.from_user.id,
                        item_id=f"{invoice.payload} month",
                        payment_amount=invoice.amount,
                        payment_type="CryptoFiatRub"
        )

        server_task_successful = server_response.get("success")

        if not server_task_successful or server_task_successful == False:
            await crypto.transfer(
                user_id=callback_query.from_user.id,
                amount=invoice.amount,
                asset=invoice.paid_asset,
                spend_id=f"refund_inv_{invoice.invoice_id}"
            )
            await bot.send_message(
                chat_id=int(callback_query.from_user.id),
                text="Произошла ошибка, поэтому мы вернули Ваши средства.",
                reply_markup=get_balance_keyboard()
            )
        else:
            await callback_query.message.answer(
                text=f"Баланс успешно пополнен на {int(invoice.amount)} RUB!",
                message_effect_id="5046509860389126442",
                reply_markup=get_main_menu_keyboard()
            )


    elif invoice.status == 'active':
        await callback_query.answer("⏳ Оплата пока не обнаружена. Попробуйте еще раз через пару секунд.", show_alert=True)

    elif invoice.status == 'expired':
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer("❌ Время действия счета истекло. Создайте новый.", show_alert=True)
