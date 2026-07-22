from aiogram import Router
from .commands import router as commands_router
from .subscriptions import router as subs_router
from .balance import router as balance_router
from .pricelist import router as pricelist_router
from .status import router as status_router

main_router = Router()
main_router.include_routers(
    commands_router,
    subs_router,
    balance_router,
    pricelist_router,
    status_router
)
