import json
import os

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
class VpnConfig(BaseModel):
    inbounds: list[int] = json.loads(os.getenv("VPN_INBOUNDS", "[6,7,8]"))
    limit_ip: int = os.getenv("VPN_LIMIT_IP")