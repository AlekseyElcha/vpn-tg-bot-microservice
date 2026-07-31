from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.bot import BotConfig
from src.config.payment import PaymentConfig
from src.config.rabbitmq import RabbitMQConfig
from src.config.redis import RedisConfig
from src.config.vpn import VpnConfig


class Settings(BaseSettings):
    bot: BotConfig
    redis: RedisConfig
    payment: PaymentConfig
    vpn: VpnConfig
    rabbitmq: RabbitMQConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )

settings = Settings()
