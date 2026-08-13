import time
from urllib import response

from aiogram import Router, types

from src.keyboards.menu import get_main_menu_keyboard
from src.services.backend_api import api_client

router = Router()

@router.callback_query(lambda c: c.data == "service_status_btn_click")
async def process_balance_menu(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    api_ping_start = time.perf_counter()
    api_ping_data = await api_client.ping_backend()
    api_ping_finish = time.perf_counter()

    if api_ping_data:
        api_status = "доступен 🟢"
    else:
        api_status = "недоступен 🔴"

    api_ping_ms = int((api_ping_finish - api_ping_start) * 1000)
    if api_ping_ms <= 250:
        api_ping_ms = str(api_ping_ms)
        api_ping_ms += " мс 🟢"
    elif api_ping_ms <= 500:
        api_ping_ms = str(api_ping_ms)
        api_ping_ms += " мс 🟡"
    elif api_ping_ms > 500 and  "недо" not in api_status:
        api_ping_ms = str(api_ping_ms)
        api_ping_ms += " мс 🟠"
    else:
        api_ping_ms = str(api_ping_ms)
        api_status += " мс 🔴"

    vpn_server_ping = await api_client.ping_vpn_server()
    server_data = await api_client.fetch_server_status()

    server_status = ""
    xray_status = ""
    admin_comment = ""

    if server_data.get("server_running"):
        server_status = "доступен 🟢"
    else:
        server_status = "недоступен 🔴"

    if server_data.get("xray_running"):
        xray_status = "запущен 🟢"
    else:
        xray_status = "не запущен 🔴"

    if server_data.get("comment"):
        admin_comment = server_data.get("comment")
    else:
        admin_comment = "нет информации 🔸"

    if vpn_server_ping and vpn_server_ping.get("success") == True:
        vpn_ping_ms = vpn_server_ping.get("ping")
        if vpn_ping_ms <= 80:
            vpn_ping_ms = str(vpn_ping_ms)
            vpn_ping_ms += " мс 🟢"
        elif vpn_ping_ms <= 250:
            vpn_ping_ms = str(vpn_ping_ms)
            vpn_ping_ms += " мс 🟡"
        elif vpn_ping_ms <= 500 and "недо" not in vpn_ping_ms:
            vpn_ping_ms = str(vpn_ping_ms)
            vpn_ping_ms += " мс 🟠"
        else:
            vpn_ping_ms = str(vpn_ping_ms)
            vpn_ping_ms += " мс 🔴"
    else:
        vpn_ping_ms = "no info 🔸"


    server_info_text = ("<b>• Статус сервиса:</b>\n\n"
                       f"<b>• VPN-сервер: {server_status}</b>\n"
                        f"└── ping: {vpn_ping_ms}\n\n"
                        f"<b>• Xray: {xray_status}</b>\n\n"
                        f"<b>• API: {api_status}</b>\n"
                        f"└── ping: {api_ping_ms}\n\n"
                        f"<b>• Комментарий: {admin_comment}</b>")


    await callback_query.message.answer(
        text=server_info_text,
        reply_markup=await get_main_menu_keyboard(callback_query.from_user.id),
        parse_mode="HTML"
    )
    await callback_query.answer()


