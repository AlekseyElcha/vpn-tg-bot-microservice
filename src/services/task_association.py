from src.notifications.send_message import send_message_to_user
from src.services.set_ratios import set_currency_ratios

TASKS = {
    "notify": send_message_to_user,
    "set_crypto_ratios": set_currency_ratios
}


def extract_action_from_payload(payload: dict):
    action = payload.get("action")
    return action