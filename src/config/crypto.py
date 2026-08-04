from pydantic import BaseModel


class CryptoConfig(BaseModel):
    token: str
