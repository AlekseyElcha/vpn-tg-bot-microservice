from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.config.settings import settings
from src.loader import bot
from src.keyboards.menu import get_main_menu_keyboard
from src.logs import logger

router = Router()

class SupportState(StatesGroup):
    waiting_for_message = State()

@router.callback_query(F.data == "support_btn_click")
async def process_support_click(callback_query: types.CallbackQuery, state: FSMContext):
    if not settings.bot.support_group_id:
        await callback_query.answer("Техподдержка временно недоступна.", show_alert=True)
        return
        
    await callback_query.message.edit_text(
        "📝 <b>Техподдержка</b>\n\n"
        "Пожалуйста, подробно опишите вашу проблему в одном сообщении ниже.\n\n"
        "<i>Для отмены нажмите кнопку «В главное меню» под любым сообщением.</i>",
        reply_markup=get_main_menu_keyboard()
    )
    await state.set_state(SupportState.waiting_for_message)
    await callback_query.answer()


@router.message(SupportState.waiting_for_message, F.text)
async def process_support_message(message: types.Message, state: FSMContext):
    if not settings.bot.support_group_id:
        await message.answer("Техподдержка временно недоступна.")
        await state.clear()
        return

    user_info = f"Пользователь: {message.from_user.full_name} (@{message.from_user.username})\nID: {message.from_user.id}"
    
    try:
        # Отправляем инфо в группу
        sent_info = await bot.send_message(
            chat_id=settings.bot.support_group_id,
            text=f"🆘 <b>Новый тикет поддержки</b>\n\n{user_info}"
        )
        # Пересылаем само сообщение юзера
        await bot.forward_message(
            chat_id=settings.bot.support_group_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        
        await message.answer(
            "✅ <b>Ваше обращение успешно отправлено!</b>\n\n"
            "Специалист поддержки ответит вам прямо в этом боте в ближайшее время.",
            reply_markup=get_main_menu_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке тикета в группу: {e}")
        await message.answer(
            "❌ Не удалось отправить обращение. Попробуйте позже.",
            reply_markup=get_main_menu_keyboard()
        )
        
    await state.clear()


# Обработчик ответов админов из группы поддержки
@router.message(F.chat.id == settings.bot.support_group_id)
async def process_admin_reply(message: types.Message):
    # Если это ответ на пересланное сообщение
    if message.reply_to_message and message.reply_to_message.forward_origin:
        origin = message.reply_to_message.forward_origin
        
        # Проверяем, что сообщение было переслано от пользователя
        if hasattr(origin, 'sender_user') and origin.sender_user:
            user_id = origin.sender_user.id
            
            try:
                if message.text:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"👨‍💻 <b>Ответ от поддержки:</b>\n\n{message.text}"
                    )
                else:
                    await bot.copy_message(
                        chat_id=user_id,
                        from_chat_id=message.chat.id,
                        message_id=message.message_id
                    )
            except Exception as e:
                logger.error(f"Не удалось отправить ответ пользователю {user_id}: {e}")
                await message.reply("❌ Не удалось доставить ответ пользователю (возможно, он заблокировал бота).")
