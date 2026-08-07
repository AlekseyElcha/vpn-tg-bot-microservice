from aiogram import Router
from .commands import router as commands_router
from .subscriptions import router as subs_router
from .balance import router as balance_router
from .pricelist import router as pricelist_router
from .status import router as status_router
from .promocodes import router as promocode_router
from .referrals import router as referrals_router
from .messaging import router as message_router
# from .crypto_payment import router as crypto_router
from .game import router as game_router
# from .fiat_payment import router as fiat_payment_router
from .payment.manage_payment import router as payment_router

main_router = Router()
main_router.include_routers(
    payment_router,
    commands_router,
    subs_router,
    balance_router,
    pricelist_router,
    status_router,
    promocode_router,
    referrals_router,
    message_router,
    # crypto_router,
    game_router,
    # fiat_payment_router,
)
