from pydantic import BaseModel


class LogsConfig(BaseModel):
    level: str
