from aiogram import Router
from .commands import router as commands_router
from .subscriptions import router as subs_router
from .balance import router as balance_router
from .pricelist import router as pricelist_router
from .status import router as status_router
from .promocodes import router as promocode_router
from .referrals import router as referrals_router

main_router = Router()
main_router.include_routers(
    commands_router,
    subs_router,
    balance_router,
    pricelist_router,
    status_router,
    promocode_router,
    referrals_router
)
