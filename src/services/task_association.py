from src.notifications.send_message import send_message_to_user

TASKS = {
    "notify": send_message_to_user
}


def extract_action_from_payload(payload: dict):
    action = payload.get("action")
    return action