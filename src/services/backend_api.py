import time
from typing import Dict, Any, List, Optional
import httpx

from src.redis_client.get_redis import get_redis_client
from src.config.settings import settings
from src.logs import logger
import os

class BackendAPIClient:
    def __init__(self, base_url: str = None):
        # self.base_url = base_url or os.getenv("BACKEND_URL", "http://localhost:8000")
        self.base_url = base_url or os.getenv("BACKEND_URL", "backend:8000")
        self.headers = {
            "X-API-Key": settings.api_security.api_secret_key
        }
        self.timeout = 5.0

    async def _make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Optional[Any]:
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        async with httpx.AsyncClient(headers=self.headers) as client:
            try:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                
                if response.status_code in [200, 201, 400]:
                    try:
                        return response.json()
                    except ValueError:
                        return response.text
                return None
            except httpx.HTTPError as e:
                logger.error(f"HTTPError on {method} {url}: {e}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error on {method} {url}: {e}")
                return None

    async def fetch_user_subscriptions(self, tg_id: int) -> List[Dict[str, Any]] | None:
        return await self._make_request("GET", "/users/subs", params={"tg_id": tg_id})

    async def fetch_subscription_info(self, email: str) -> Optional[Dict[str, Any]]:
        return await self._make_request("GET", "/clients/info", params={"email": email})

    async def fetch_subscription_link(self, email: str) -> str:
        response = await self._make_request("GET", "/clients/link", params={"email": email})
        if response and response.get("msg") == "success":
            return response.get("link", "Не удалось получить ссылку...")
        return "None - подписка не найдена!"

    async def delete_subscription(self, email: str) -> Dict[str, str]:
        response = await self._make_request("POST", f"/clients/delete/{email}", params={"keep_traffic": 0})
        if response and response.get("msg") == "success":
            return response
        return {"msg": "Не удалось удалить подписку."}

    async def fetch_user_balance(self, tg_id: int) -> float | None:
        response = await self._make_request("GET", "/users/balance", params={"tg_id": tg_id})
        if response:
            return response.get("balance")
        return None

    async def fetch_server_post_payment_task_result(
        self, user_id: int, item_id: str, payment_amount: float, payment_type: str
    ) -> Dict[str, Any] | None:
        json_data = {
            "user_id": user_id,
            "item_id": item_id,
            "payment_amount": payment_amount,
            "payment_type": payment_type,
        }
        return await self._make_request("POST", "/payment/pay", json=json_data)

    async def create_subscription(
        self, email: str, total_gb: int | float, expiry_time: int, tg_id: int, 
        limit_ip: int, enable: bool, inbounds: list[int], is_trial: bool
    ) -> Optional[Dict[str, Any]]:
        json_data = {
            "new_client": {
                "client": {
                    "email": email,
                    "total_gb": total_gb,
                    "expiry_time": expiry_time,
                    "tg_id": tg_id,
                    "limit_ip": limit_ip,
                    "enable": enable
                },
                "inbound_ids": inbounds
            },
            "is_trial": is_trial
        }
        return await self._make_request("POST", "/clients/add", json=json_data)

    async def fetch_server_status(self) -> Optional[Dict[str, Any]]:
        return await self._make_request("GET", "/server/status")

    async def ping_vpn_server(self) -> Optional[Dict[str, Any]]:
        return await self._make_request("GET", "/check/ping-vpn-server")

    async def create_new_user(self, tg_id: int | float, balance: int) -> Optional[Dict[str, Any]]:
        json_data = {"tg_id": tg_id, "balance": balance}
        return await self._make_request("POST", "/users/add", json=json_data)

    async def ping_backend(self):
        return await self._make_request("GET", "/server/status")

    async def activate_bonus_code(self, code: str, tg_id: int) -> Dict[str, Any]:
        response = await self._make_request("GET", "/promo/activate", params={"code": code, "tg_id": tg_id})
        if response:
            return response
        return {"success": False, "msg": "Не удалось активировать промокод."}

    async def activate_referral(self, referred_tg_id: int, referral_code: str) -> Optional[Dict[str, Any]]:
        response = await self._make_request(
            "POST", "/referral/activate", 
            params={"referral_code": referral_code, "referred_tg_id": referred_tg_id}
        )
        if response and response.get("success") and response.get("msg"):
            return response
        return None

    async def fetch_referral_link(self, tg_id: int) -> Optional[Dict[str, Any]]:
        response = await self._make_request("GET", "/referral/link", params={"tg_id": tg_id})
        if response and response.get("success") and response.get("referral_link"):
            return response
        return None

    async def fetch_all_user_tg_ids(self) -> Optional[Dict[str, Any]]:
        return await self._make_request("GET", "/users/ids")

    async def fetch_crypto_currency_ratio(self, currency_code: str) -> Optional[float]:
        response = await self._make_request("GET", "/currencies/get", params={"currency_code": currency_code})
        if response and response.get("success") and response.get("currency_ratio"):
            return response.get("currency_ratio")
        return None

    async def fetch_crypto_currency_ratio_v2(self, currency_code: str) -> Optional[int]:
        async with get_redis_client() as redis_client:
            cache_key = f"ratio:{currency_code}"
            current_ratio = await redis_client.get(cache_key)
            if current_ratio:
                return int(current_ratio)
            return None

    async def fetch_crypto_currency_ratio_many(self, currency_names: list) -> Optional[Dict[str, Any]]:
        return await self._make_request("GET", "/currencies/many", params={"currency_names": currency_names}, timeout=45.0)

    async def fetch_daily_game_streak(self, tg_id: int) -> int | None:
        response = await self._make_request("GET", "/game/streak", params={"tg_id": tg_id}, timeout=15.0)
        if response:
            return response.get("streak")
        return None

    async def register_check_in_daily_game(self, tg_id: int) -> str | None:
        response = await self._make_request("POST", "/game/check-in", params={"tg_id": tg_id}, timeout=15.0)
        if response:
            return response.get("msg")
        return None

    async def check_trial_validity(self, tg_id: int) -> bool | None:
        response = await self._make_request(method="GET", endpoint="/users/trial_validity", params={"tg_id": tg_id}, timeout=15.0)
        if response:
            return response.get("is_valid")
        return None

    # async def activate_trial_in_db(self, tg_id: int) -> bool | None:
    #


api_client = BackendAPIClient()
