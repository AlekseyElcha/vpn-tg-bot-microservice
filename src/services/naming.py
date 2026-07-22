import typing
import uuid


def create_subscription_name_by_tg_id(
        tg_id: int
) -> str:
    sub_name = f"{tg_id}-{str(uuid.uuid4())[:4]}"

    return sub_name