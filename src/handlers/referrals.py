from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest

from src.keyboards.menu import get_main_menu_keyboard
from src.services.backend_api import api_client

router = Router()

@router.callback_query(lambda c: c.data == "referrals_btn_click")
async def process_referrals_btn_click(
        callback_query: types.CallbackQuery
):
    try:
        ref_link_req_resp = await api_client.fetch_referral_link(tg_id=callback_query.from_user.id)
        if not ref_link_req_resp or not ref_link_req_resp.get("success"):
            await callback_query.message.edit_text(
                text=f"Произошла ошибка!",
                reply_markup=get_main_menu_keyboard()
            )
            await callback_query.answer()

        ref_link = ref_link_req_resp.get("referral_link")

        instruction_with_link = (
            f"<b>Представляем реферальную систему УруруVPN!</b>\n\n"
            f"Делитесь своей ссылкой, Вы и Ваш друг получите бонусы!\n\n"
            f"Друг получит бонусный баланс, а Вы будете получать процент от пополений друга на Ваш аккаунт!\n\n"
            f"Ваша ссылка: <code>{ref_link}</code>"
        )

        await callback_query.message.edit_text(
            text=instruction_with_link,
            reply_markup=get_main_menu_keyboard()
        )

        await callback_query.answer()
    except TelegramBadRequest:
        pass