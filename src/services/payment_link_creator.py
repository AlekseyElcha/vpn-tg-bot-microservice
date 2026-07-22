from aiogram import types
from pydantic import BaseModel

from src.loader import bot


class PaymentData(BaseModel):
    user_id: int
    item_id: str
    price_stars: int | float



async def create_payment_link(payment_data: PaymentData):
    try:
        invoice_link = await bot.create_invoice_link(
            title="Оплата услуг УруруVPN",
            description=f"Оплата товара {payment_data.item_id}",
            payload=f"pay:{payment_data.user_id}:{payment_data.item_id}",
            provider_token="",
            currency="XTR",
            prices=[
                types.LabeledPrice(label="Stars", amount=payment_data.price_stars)
            ]
        )
        return {
            "pay_url": invoice_link
        }
    except Exception as e:
        return None