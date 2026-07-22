from aiogram import types, Router
from aiogram.exceptions import TelegramBadRequest

from src.config.settings import settings
from src.keyboards.menu import get_main_menu_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "pricelist_btn_click")
async def process_pricelist_btn_click(
        callback_query: types.CallbackQuery,
):
    try:
        price_info = ("<b>Наши тарифы:</b>\n\n"
                      "На самом деле у нас всё предельно просто и понятно.\n\n"
                      "Наш сервис действует по принципу - <b>пополняй баланс и пользуйся</b>.\n\n"
                      "Что это значит?\n\n"
                      "<b>Вы пополняете баланс через этого бота, оплата происходит в Telegram Stars.\n\n"
                      "Эти средства начисляются на Ваш личный кабинет.\n\n"
                      "Далее Вы создаете подписки, импортируйте их на свои устройства</b>\n\n"
                      "Наши конфигурации работают как на Android и IOS, так и на Windows, macOS и Linux.\n\n"
                      "Одновременно можно использовать только <b>1 устройство</b>!"
                      f"Каждый день на сервере происходит списание в {settings.payment.daily_price} Stars с Вашего личного кабинета.\n\n"
                      "Как только баланс становится ≤ 0, Ваши подписки будут отключены (НЕ удаляются!)\n\n"
                      "Как только баланс вновь станет положительным - оказание услуг возобновится!"
        )

        await callback_query.message.edit_text(
            text=price_info,
            reply_markup=get_main_menu_keyboard()
        )
        await callback_query.answer()
    except TelegramBadRequest:
        await callback_query.answer()
