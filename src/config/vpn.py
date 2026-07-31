from pydantic import BaseModel


class VpnConfig(BaseModel):
    inbounds: list[int]
    limit_ip: int