# from aiocryptopay import AioCryptoPay , Networks
# from aiocryptopay.exceptions import CryptoPayAPIError
# from aiogram import Router, F, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder
#
# from src.keyboards.menu import get_balance_keyboard, get_main_menu_keyboard
# from src.loader import bot
# from src.services.backend_api import api_client
# from src.services.currency_exchange import exchange_crypto_to_tg_stars
#
# router = Router()
#
#
# @router.callback_query(lambda c: c.data == "add_money_crypto_btn_click")
# async def process_add_money_btn_click(
#         callback_query: types.CallbackQuery
# ):
#     builder = InlineKeyboardBuilder()
#
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"GRAM (ex. Toncoin) 💎",
#             callback_data=f"choose_crypto_ton"
#         )
#     )
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"Tether (USDT) 💰",
#             callback_data=f"choose_crypto_usdt"
#         )
#     )
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"TRON (TRX) [тест получения из Redis]",
#             callback_data=f"choose_crypto_trx"
#         )
#     )
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"⬅️ Назад",
#             callback_data=f"my_balance_btn_click"
#         )
#     )
#     await callback_query.message.edit_text(
#         text=f"<b>Выберите криптовалюту:</b>",
#         reply_markup=builder.as_markup()
#     )
#
#     await callback_query.answer()
#
#
#
# # @router.callback_query(lambda c: c.data == "add_money_crypto_btn_click")
# # async def process_add_money_btn_click(
# #         callback_query: types.CallbackQuery
# # ):
# #     builder = InlineKeyboardBuilder()
# #
# #     builder.row(
# #         types.InlineKeyboardButton(
# #             text=f"1 TON ~ 100🌟",
# #             callback_data=f"add_crypto_0.1_TON"
# #         )
# #     )
# #     builder.row(
# #         types.InlineKeyboardButton(
# #             text=f"2 TON ~ 200🌟",
# #             callback_data=f"add_crypto_0.2_TON"
# #         )
# #     )
# #     builder.row(
# #         types.InlineKeyboardButton(
# #             text=f"3 TON ~ 300🌟",
# #             callback_data=f"add_crypto_0.3_TON"
# #         )
# #     )
# #
# #     builder.row(
# #         types.InlineKeyboardButton(
# #             text=f"⬅️ Назад",
# #             callback_data=f"my_balance_btn_click"
# #         )
# #     )
# #
# #     await callback_query.message.edit_text(
# #         text=f"Выберите сумму для пополнения:",
# #         reply_markup=builder.as_markup()
# #     )
# #
# #     await callback_query.answer()
#
#
# @router.callback_query(F.data.startswith("choose_crypto_ton"))
# async def process_pay_crypto_btn_click(
#         callback_query: types.CallbackQuery,
# ):
#     ratio = await api_client.fetch_crypto_currency_ratio(
#         currency_code="TON"
#     )
#
#     builder = InlineKeyboardBuilder()
#
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"1 TON ~ {ratio * 1}🌟",
#             callback_data=f"add_crypto_0.1_TON"
#         )
#     )
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"2 TON ~ {ratio * 2}🌟",
#             callback_data=f"add_crypto_0.2_TON"
#         )
#     )
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"3 TON ~ {ratio * 3}🌟",
#             callback_data=f"add_crypto_0.3_TON"
#         )
#     )
#
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"⬅️ Назад",
#             callback_data=f"add_money_crypto_btn_click"
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
# @router.callback_query(F.data.startswith("choose_crypto_usdt"))
# async def process_pay_crypto_btn_click(
#         callback_query: types.CallbackQuery,
# ):
#     ratio = await api_client.fetch_crypto_currency_ratio(
#         currency_code="USDT"
#     )
#
#
#     builder = InlineKeyboardBuilder()
#
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"1 USDT ~ {ratio * 1}🌟",
#             callback_data=f"add_crypto_1_USDT"
#         )
#     )
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"2 USDT ~ {ratio * 2}🌟",
#             callback_data=f"add_crypto_2_USDT"
#         )
#     )
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"3 USDT ~ {ratio * 3}🌟",
#             callback_data=f"add_crypto_3_USDT"
#         )
#     )
#
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"⬅️ Назад",
#             callback_data=f"add_money_crypto_btn_click"
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
# @router.callback_query(F.data.startswith("choose_crypto_trx"))
# async def process_pay_crypto_btn_click(
#         callback_query: types.CallbackQuery,
# ):
#     ratio = await api_client.fetch_crypto_currency_ratio_v2(
#         currency_code="TRX"
#     )
#
#     if not ratio:
#         await callback_query.message.edit_text(
#             text=f"Курсы криптовалют обновляются, повторите попытку позже...",
#             reply_markup=get_balance_keyboard()
#         )
#
#     builder = InlineKeyboardBuilder()
#
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"3 TRX ~ {ratio * 3}🌟",
#             callback_data=f"add_crypto_3_TRX"
#         )
#     )
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"6 TRX ~ {ratio * 6}🌟",
#             callback_data=f"add_crypto_6_TRX"
#         )
#     )
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"9 TRX ~ {ratio * 9}🌟",
#             callback_data=f"add_crypto_9_TRX"
#         )
#     )
#
#     builder.row(
#         types.InlineKeyboardButton(
#             text=f"⬅️ Назад",
#             callback_data=f"add_money_crypto_btn_click"
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
#
# @router.callback_query(F.data.startswith("add_crypto_"))
# async def process_pay_crypto_btn_click(
#         callback_query: types.CallbackQuery,
#         crypto: AioCryptoPay
# ):
#     amount = float(callback_query.data.split("_")[2])
#     asset = callback_query.data.split("_")[3]
#
#     payment_invoice = await crypto.create_invoice(
#         asset=asset,
#         amount=amount,
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
#
#
# # @router.callback_query(F.data.startswith("check_"))
# # async def check_payment_status(
# #         callback_query: types.CallbackQuery,
# #         crypto: AioCryptoPay
# # ):
# #     invoice_id = int(callback_query.data.split("_")[1])
# #
# #     invoices = await crypto.get_invoices(invoice_ids=invoice_id)
# #
# #     invoice = invoices[0] if isinstance(invoices, list) else invoices
# #
# #     if invoice.status == 'paid':
# #         await callback_query.message.edit_reply_markup(reply_markup=None)
# #
# #         await callback_query.answer("🎉 Оплата прошла успешно!", show_alert=True)
# #
# #         payment_amount = await exchange_crypto_to_tg_stars(
# #             crypto_name=invoice.asset,
# #             crypto_amount=invoice.amount
# #         )
# #
# #         if not payment_amount:
# #             spend_id = f"refund_inv_{invoice.invoice_id}"
# #             await crypto.transfer(
# #                 user_id=callback_query.from_user.id,
# #                 amount=invoice.amount,
# #                 asset=invoice.asset,
# #                 spend_id=spend_id
# #             )
# #
# #
# #         server_response = await api_client.fetch_server_post_payment_task_result(
# #             user_id=callback_query.from_user.id,
# #             item_id=f"{invoice.amount} {invoice.asset}",
# #             payment_amount=payment_amount
# #         )
# #
# #         if server_response is None:
# #             await crypto.transfer(
# #                 user_id=callback_query.from_user.id,
# #                 amount=invoice.amount,
# #                 asset=invoice.asset,
# #                 spend_id=f"refund_inv_{invoice.invoice_id}"
# #             )
# #             await bot.send_message(
# #                 chat_id=int(callback_query.from_user.id),
# #                 text="Что-то пошло не так, поэтому мы вернули Ваши средства.",
# #                 reply_markup=get_balance_keyboard()
# #             )
# #
# #         server_task_successful = server_response.get("success")
# #
# #         if not server_task_successful or server_task_successful == False:
# #             await crypto.transfer(
# #                 user_id=callback_query.from_user.id,
# #                 amount=invoice.amount,
# #                 asset=invoice.asset,
# #                 spend_id=f"refund_inv_{invoice.invoice_id}"
# #             )
# #             await bot.send_message(
# #                 chat_id=int(callback_query.from_user.id),
# #                 text="Произошла ошибка, поэтому мы вернули Ваши средства.",
# #                 reply_markup=get_balance_keyboard()
# #             )
# #
# #         payment_test_mode_enabled = True
# #         if payment_test_mode_enabled:
# #             try:
# #                 await crypto.transfer(
# #                     user_id=callback_query.from_user.id,
# #                     amount=invoice.amount,
# #                     asset=invoice.asset,
# #                     spend_id=f"refund_inv_{invoice.invoice_id}"
# #                 )
# #             except Exception as e:
# #                 print(f"Не удалось выполнить автовозврат: {e}")
# #
# #         await bot.send_message(
# #             chat_id=int(callback_query.from_user.id),
# #             text=f"<b>Ура! 🎉\n\n"
# #                  f"На баланс Вашего аккаунта успешно зачислено {payment_amount}🌟\n\n"
# #                  f"Благодарим за пользование услугами УруруVPN!</b>",
# #             reply_markup=get_balance_keyboard(),
# #             message_effect_id="5046509860389126442"
# #         )
#
# @router.callback_query(F.data.startswith("check_"))
# async def check_payment_status(
#         callback_query: types.CallbackQuery,
#         crypto: AioCryptoPay
# ):
#     invoice_id = int(callback_query.data.split("_")[1])
#
#     invoices = await crypto.get_invoices(invoice_ids=invoice_id)
#
#     if not invoices:
#         await callback_query.answer("Счет не найден.", show_alert=True)
#         return
#
#     invoice = invoices[0] if isinstance(invoices, list) else invoices
#
#
#     if invoice.status == 'paid':
#         await callback_query.message.edit_reply_markup(reply_markup=None)
#         await callback_query.answer("🎉 Оплата прошла успешно!", show_alert=True)
#
#         if invoice.asset == "123": #TODO убрать!!!
#             return
#
#         payment_amount = await exchange_crypto_to_tg_stars(
#             crypto_name=invoice.asset,
#             crypto_amount=invoice.amount
#         )
#
#         server_response = await api_client.fetch_server_post_payment_task_result(
#                         user_id=callback_query.from_user.id,
#                         item_id=f"{invoice.amount} {invoice.asset}",
#                         payment_amount=payment_amount
#         )
#
#         server_task_successful = server_response.get("success")
#
#         if not server_task_successful or server_task_successful == False:
#             await crypto.transfer(
#                 user_id=callback_query.from_user.id,
#                 amount=invoice.amount,
#                 asset=invoice.asset,
#                 spend_id=f"refund_inv_{invoice.invoice_id}"
#             )
#             await bot.send_message(
#                 chat_id=int(callback_query.from_user.id),
#                 text="Произошла ошибка, поэтому мы вернули Ваши средства.",
#                 reply_markup=get_balance_keyboard()
#             )
#         else:
#             await callback_query.message.answer(
#                 text=f"Баланс успешно пополнен на {int(payment_amount)}🌟!",
#                 message_effect_id="5046509860389126442",
#                 reply_markup=get_main_menu_keyboard()
#             )
#
#
#     elif invoice.status == 'active':
#         await callback_query.answer("⏳ Оплата пока не обнаружена. Попробуйте еще раз через пару секунд.", show_alert=True)
#
#     elif invoice.status == 'expired':
#         await callback_query.message.edit_reply_markup(reply_markup=None)
#         await callback_query.answer("❌ Время действия счета истекло. Создайте новый.", show_alert=True)
