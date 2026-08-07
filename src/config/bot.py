from pydantic import BaseModel


class BotConfig(BaseModel):
    token: str
    proxy: str
    test_mode_enabled: bool
    service_mode_enabled: int # 0 / 1
    service_mode_text: str
    limit_seconds: int
    admin_ids: list[int] = []
    support_group_id: int | None = None
