from pydantic import BaseModel


class RabbitMQConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
