from pydantic_settings import BaseSettings

from src.config.bot import BotConfig
from src.config.payment import PaymentConfig
from src.config.redis import RedisConfig
from src.config.vpn import VpnConfig


class Settings(BaseSettings):
    bot: BotConfig = BotConfig()
    redis: RedisConfig = RedisConfig()
    payment: PaymentConfig = PaymentConfig()
    vpn: VpnConfig = VpnConfig()

settings = Settings()
