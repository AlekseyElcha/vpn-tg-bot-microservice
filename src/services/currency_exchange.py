from src.services.backend_api import api_client


async def exchange_crypto_to_tg_stars(
        crypto_name: str,
        crypto_amount: float
) -> int | float | None:
    currency_ratio = await api_client.fetch_crypto_currency_ratio(crypto_name)

    if not currency_ratio:
        return None

    stars_amount = crypto_amount * currency_ratio

    return stars_amount
