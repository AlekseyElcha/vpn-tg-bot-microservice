import os

from pydantic import BaseModel


class PaymentConfig(BaseModel):
    daily_price: int = os.getenv("DAILY_PRICE")
