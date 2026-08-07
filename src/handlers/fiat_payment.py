# from aiocryptopay import AioCryptoPay
# from aiogram import Router, types, F
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder
#
# from src.handlers import crypto_payment
#
# router = Router()
#
# @router.callback_query(lambda c: c.data == "add_money_fiat_btn_click")
# async def process_add_money_fiat_btn_click(callback_query: types.CallbackQuery):
#     builder = InlineKeyboardBuilder()
#
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"100 RUB",
#             callback_data=f"add_fiat_100_RUB"
#         )
#     )
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"200 RUB",
#             callback_data=f"add_fiat_200_RUB"
#         )
#     )
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"300 RUB",
#             callback_data=f"add_fiat_300_RUB"
#         )
#     )
#
#     await callback_query.message.edit_text(
#         text=f"Выберите сумму для пополнения:",
#         reply_markup=builder.as_markup()
#     )
#
#     await callback_query.answer()
#
#
# @router.callback_query(F.data.startswith("add_fiat_"))
# async def process_add_fiat_amount_btn_click(
#         callback_query: types.CallbackQuery,
#         crypto: AioCryptoPay
# ):
#     amount = int(callback_query.data.split("_")[2])
#
#     payment_invoice = await crypto.create_invoice(
#         currency_type="fiat",  # Строго "fiat"
#         fiat="RUB",  # Валюта ценника
#         amount=amount,  # Сумма в рублях
#         asset="123",
#         accepted_assets=["JET"],
#         description=f'Пополнение баланса УруруVPN - {amount}'
#     )
#
#     pay_kb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="💸 Оплатить в CryptoBot", url=payment_invoice.bot_invoice_url)],
#         [InlineKeyboardButton(text="🔄 Проверить оплату", callback_data=f"check_{payment_invoice.invoice_id}")]
#     ])
#
#     await callback_query.message.answer(
#         f"Счет успешно сгенерирован!\n"
#         f"Сумма: <b>{payment_invoice.amount} {payment_invoice.asset}</b>\n\n"
#         f"После оплаты <b>обязательно</b> нажмите кнопку <b>«Проверить оплату»</b> ниже.",
#         reply_markup=pay_kb,
#         parse_mode="HTML"
#     )
#
#     await callback_query.answer()