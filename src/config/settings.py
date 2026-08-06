from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.bot import BotConfig
from src.config.crypto import CryptoConfig
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
    crypto: CryptoConfig
    api_secret_key: str = "your-super-secret-key-change-it-in-production"
    yookassa_shop_id: str = "123456" # TODO:потом заменить на настоящий ID магазина
    yookassa_secret_key: str = "test_xxxxxx" # TODO: потом заменить на настоящий ключ
    yookassa_return_url: str = "https://t.me/ваша_ссылка_на_бота"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )

settings = Settings()
