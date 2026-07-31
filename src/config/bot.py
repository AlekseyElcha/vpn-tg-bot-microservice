from pydantic import BaseModel


class BotConfig(BaseModel):
    token: str
    proxy: str
    test_mode_enabled: bool
