from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from src.config.settings import settings

bot_token = settings.bot.token

session = AiohttpSession(proxy=settings.bot.proxy)

bot = Bot(
    token=bot_token,
    session=session,
    default=DefaultBotProperties(parse_mode="HTML"),
)

dp = Dispatcher()
