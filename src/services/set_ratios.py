from src.redis_client.get_redis import get_redis_client
from src.services.backend_api import api_client


async def set_currency_ratios(
        rmq_payload: dict
) -> bool:
    print("Начато обновление...")
    error_currencies = []

    async with get_redis_client() as redis_cl:
        currency_dict = rmq_payload.get("data", {})
        for code, ratio in currency_dict.items():
            redis_key = f"ratio:{code}"
            print(redis_key)

            if ratio == -1:
                error_currencies.append(code)

            else:
                await redis_cl.delete(redis_key)
                await redis_cl.set(redis_key, ratio, ex=3800)

        if error_currencies:
            error_fixed_results = await api_client.fetch_crypto_currency_ratio_many(
                currency_names=error_currencies
            )

            for item in error_fixed_results:
                code = item.get("currency_code")
                ratio = item.get("exchange_rate")
                redis_key = f"ratio:{code}"
                if ratio == -1:
                    error_currencies.remove(item)
                    await redis_cl.set(redis_key, ratio, ex=3800)


        if error_currencies:
            for code, _ in error_currencies:
                redis_key = f"ratio:{code}"
                current_ratio = await redis_cl.get(redis_key)
                await redis_cl.delete(redis_key)
                await redis_cl.set(redis_key, current_ratio, ex=3800)
    print("Обноление завершено!")
    return True
