import os

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
class RedisConfig(BaseModel):
    host: str = os.getenv("REDIS_HOST")
    port: int = os.getenv("REDIS_PORT")
