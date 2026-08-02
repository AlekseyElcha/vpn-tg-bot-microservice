from aiogram import Router, types, F
from aiogram.filters import CommandStart, CommandObject, Command

from src.keyboards.menu import get_main_menu_keyboard, get_main_admin_keyboard
from src.loader import bot
from src.services.backend_api import api_client

router = Router()

@router.message(CommandStart())
async def process_start_command(
        message: types.Message,
        command: CommandObject
):
    # service_mode_enabled = True if settings.bot.service_mode_enabled == 1 else False
    #
    # if service_mode_enabled:
    #     service_msg = settings.bot.service_mode_text
    #     bot.send_message(
    #         chat_id=message.chat.id,
    #         text="<b>Сервис находится на тех.обслуживании!<b>\n" + service_msg
    #     )
    #     return

    ref_code = command.args
    user_tg_id = message.from_user.id

    if ref_code:
        resp = await api_client.activate_referral(
            referred_tg_id=user_tg_id,
            referral_code=ref_code
        )
        if resp and resp.get("success"):
            # welcome_message = (
            #     "<b>Добро пожаловать в официального бота УруруVPN!</b>\n\n"
            #     "Здесь Вы можете управлять своими подписками и пополнять баланс личного кабинета!\n\n"
            #     "Выберите нужный раздел по кнопке ниже:"
            # )

            welcome_message = resp.get("msg")

            if not resp.get("sent_via_broker"):
                referrer_id = resp.get("referrer_id")
                await bot.send_message(
                    chat_id=referrer_id,
                    text=f"Поздравляем! Вашей реферальной ссылкой успешно воспользовались!\n"
                       f"На Ваш баланс начислен бонус {1}!\n"
                       f"Спасибо Вам!"
                )

            await message.answer(
                text=welcome_message,
                reply_markup=get_main_menu_keyboard()
            )
            return



    response = await api_client.create_new_user(
        tg_id=user_tg_id,
        balance=0
    )

    if response and response.get("success"):
        welcome_message = (
            "<b>Добро пожаловать в официального бота УруруVPN!</b>\n\n"
            "Здесь Вы можете управлять своими подписками и пополнять баланс личного кабинета!\n\n"
            "Выберите нужный раздел по кнопке ниже:"
        )

        await message.answer(
            text=welcome_message,
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await message.answer(
            text="Добро пожаловать! Выберите необходимое действие:",
            reply_markup=get_main_menu_keyboard()
        )

ADMIN_IDS = [5696529637]
@router.message(Command("admin"), F.from_user.id.in_(ADMIN_IDS))
async def process_admin_command(message: types.Message):
    await message.answer(
        text="<b>Выберите действие:</b>",
        reply_markup=get_main_admin_keyboard(),
    )


@router.callback_query(lambda c: c.data == "back_to_main")
async def process_back_to_main(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text="<b>Выберите действие:</b>",
        reply_markup=get_main_menu_keyboard()
    )
    await callback_query.answer()
