import time
from urllib import response

from aiogram import Router, types

from src.keyboards.menu import get_main_menu_keyboard
from src.services.backend_api import api_client

router = Router()

@router.callback_query(lambda c: c.data == "service_status_btn_click")
async def process_balance_menu(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    server_info_text = "<b>Статус сервиса:</b>\n\n"

    server_info = await api_client.fetch_server_status()

    backend_ping_start = time.perf_counter()

    res = await api_client.ping_backend()
    if res:
        backend_ping_finish = time.perf_counter()

        ping_time_ms = int((backend_ping_finish - backend_ping_start) * 1000)

        if ping_time_ms <= 50:
            api_status_text = f"⚡ {ping_time_ms} мс"
        elif ping_time_ms <= 150:
            api_status_text = f"🟢 {ping_time_ms} мс"
        else:
            api_status_text = f"🟡 {ping_time_ms} мс"
    else:
        api_status_text = "❌ Недоступен (Time Out)"


    if server_info is None:
        server_info_text += "Не удалось получить информацию..."
    else:
        server_running = "Работает 🟢" if server_info.get("server_running") else "Не работает 🔴"
        xray_running = "Работает 🟢" if server_info.get("xray_running") else "Не работает 🔴"
        comment = server_info.get("comment", "Нет комментариев")

        server_info_text += f"<b>VPN-cервер:</b> {server_running}\n"
        server_info_text += f"<b>API:</b> {api_status_text}\n"
        server_info_text += f"<b>Xray:</b> {xray_running}\n"
        server_info_text += f"<b>Комментарий:</b> {comment}"

    await callback_query.message.answer(
        text=server_info_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback_query.answer()


