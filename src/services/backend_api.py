from typing import Dict, Any, List

import httpx

from src.redis_client import get_redis
from src.redis_client.get_redis import get_redis_client


class BackendAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url


    async def fetch_user_subscriptions(self, tg_id: int) -> List[Dict[str, Any]] | None:
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/users/subs"
                response = await client.get(url, params={"tg_id": tg_id}, timeout=5.0)

                if response.status_code == 200:
                    print(response.json())
                    return response.json()
                return None

            except httpx.HTTPError as e:
                print(f"Ошибка сети при запросе к бэкенду: {e}")
                return None


    async def fetch_subscription_info(self, email: str):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/clients/info"
                response = await client.get(
                    url,
                    params={"email": email},
                    timeout=5.0
                )

                if response.status_code == 200:
                    response = response.json()
                    return response
                else:
                    print("error")
                    return None
            except httpx.HTTPError as e:
                print(f"Ошибка сети при запросе к бэкенду: {e}")
                return None


    async def fetch_subscription_link(self, email: str) -> str:
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/clients/link"
                response = await client.get(url, params={"email": email}, timeout=5.0)

                if response.status_code == 200:
                    response = response.json()
                    if response.get("msg") == "success":
                        subscription_link = response.get("link", "Не удалось получить ссылку...")
                        return subscription_link

                return "None - подписка не найдена!"

            except httpx.HTTPError as e:
                print(f"Ошибка сети при запросе к бэкенду: {e}")
                return "None - ошибка сервера..."


    async def delete_subscription(self, email: str) -> Dict[str, str]:
        async with (httpx.AsyncClient() as client):
            try:
                url = f"{self.base_url}/clients/delete/{email}"
                response = await client.post(url, params={"keep_traffic": 0}, timeout=5.0)

                if response.status_code == 200:
                    response = response.json()
                    if response.get("msg") == "success":
                        return response

                return {
                    "msg": "Не удалось удалить подписку."
                }

            except httpx.HTTPError as e:
                print(f"Ошибка сети при запросе к бэкенду: {e}")
                return {
                    "msg": "Не удалось удалить подписку."
                }


    async def fetch_user_balance(self, tg_id: int) -> float| None:
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/users/balance"
                response = await client.get(url, params={"tg_id": tg_id}, timeout=5.0)

                if response.status_code == 200:
                    response = response.json()
                    user_balance = response.get("balance")
                    return user_balance
                else:
                    return None
            except Exception as e:
                return None


    async def fetch_server_post_payment_task_result(self,
                                 user_id: int,
                                 item_id: str,
                                 payment_amount: float
    ) -> Dict[str, Any] | None:
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/payment/pay"

                json_data = {
                    "user_id": user_id,
                    "item_id": item_id,
                    "payment_amount": payment_amount
                }

                response = await client.post(url, json=json_data, timeout=5.0)
                return response.json()

            except Exception as e:
                return None


    async def create_subscription(self,
                                      email: str,
                                      total_gb: int | float,
                                      expiry_time: int,
                                      tg_id: int,
                                      limit_ip: int,
                                      enable: bool,
                                      inbounds: list[int]

    ):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/clients/add"
                json_data = {
                  "client": {
                    "email": email,
                    "total_gb": total_gb,
                    "expiry_time": expiry_time,
                    "tg_id": tg_id,
                    "limit_ip": limit_ip,
                    "enable": enable
                  },
                  "inbound_ids": inbounds
                }

                response = await client.post(url, json=json_data, timeout=5.0)
                return response.json()

            except Exception as e:
                return None


    async def fetch_server_status(self):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/server/status"

                response = await client.get(url, timeout=5.0)
                return response.json()
            except Exception as e:
                return None


    async def ping_vpn_server(self):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/check/ping-vpn-server"

                response = await client.get(url, timeout=5.0)
                return response.json()
            except Exception as e:
                return None


    async def create_new_user(self, tg_id: int | float, balance: int):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/users/add"
                json_data = {
                    "tg_id": tg_id,
                    "balance": balance
                }

                response = await client.post(url, json=json_data, timeout=5.0)
                return response.json()

            except Exception as e:
                return None 


    async def ping_backend(self):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/server/status"

                response = await client.get(url, timeout=5.0)
                return response

            except Exception as e:
                return None


    async def activate_bonus_code(self,
                                  code: str,
                                  tg_id: int
    ):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/promo/activate"
                response = await client.get(url,
                                            params=
                                            {
                                                "code": code,
                                                "tg_id": tg_id
                                            },
                                            timeout=5.0)

                try:
                    return response.json()
                except Exception as e:
                    return {
                        "success": False,
                        "msg": "error!"
                    }
            except Exception as e:
                return {
                    "success": False,
                    "msg": e
                }


    async def activate_referral(self,
                                referred_tg_id: int,
                                referral_code: str
    ):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/referral/activate"
                response = await client.post(url,
                                            params=
                                            {
                                                "referral_code": referral_code,
                                                "referred_tg_id": referred_tg_id
                                            },
                                            timeout=5.0)

                if response.status_code == 200:
                    response = response.json()
                    if response.get("success") and response.get("msg"):
                        return response
                    return None
                else:
                    return None
            except Exception as e:
                return None


    async def fetch_referral_link(self,
                                tg_id: int
    ):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/referral/link"
                response = await client.get(url,
                                            params=
                                            {
                                                "tg_id": tg_id
                                            },
                                            timeout=5.0)

                if response.status_code == 200:
                    response = response.json()
                    if response.get("success") and response.get("referral_link"):
                        return response
                    return None
                else:
                    return None
            except Exception as e:
                return None


    async def fetch_all_user_tg_ids(self):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/users/ids"

                response = await client.get(url, timeout=5.0)
                return response.json()

            except Exception as e:
                return None


    async def fetch_crypto_currency_ratio(self, currency_code: str):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/currencies/get"
                response = await client.get(url,
                                            params=
                                            {
                                                "currency_code": currency_code
                                            },
                                            timeout=5.0)

                if response.status_code == 200:
                    response = response.json()
                    if response.get("success") and response.get("currency_ratio"):
                        return response.get("currency_ratio")
                    return None
                else:
                    return None
            except Exception as e:
                return None


    async def fetch_crypto_currency_ratio_v2(self, currency_code: str):
        # через Redis
        async with get_redis_client() as redis_client:
            cache_key = f"ratio:{currency_code}"
            current_ratio = await redis_client.get(cache_key)
            if current_ratio:
                return int(current_ratio)
            else:
                return None



    async def fetch_crypto_currency_ratio_many(self, currency_names: list):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/currencies/many"

                response = await client.get(url,
                                             params={"currency_names": currency_names},
                                             timeout=45.0
                )
                return response.json()

            except Exception as e:
                return None


api_client = BackendAPIClient()
