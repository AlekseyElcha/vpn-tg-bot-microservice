import os

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
class BotConfig(BaseModel):
    token: str = os.getenv("BOT_TOKEN")
    proxy: str = os.getenv("BOT_PROXY")
    test_mode_enabled: bool = os.getenv("TEST_MODE_ENABLED")
