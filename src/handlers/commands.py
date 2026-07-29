from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject
from src.keyboards.menu import get_main_menu_keyboard
from src.services.backend_api import api_client

router = Router()

@router.message(CommandStart())
async def process_start_command(
        message: types.Message,
        command: CommandObject
):
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


@router.callback_query(lambda c: c.data == "back_to_main")
async def process_back_to_main(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text="Выберите действие:",
        reply_markup=get_main_menu_keyboard()
    )
    await callback_query.answer()
