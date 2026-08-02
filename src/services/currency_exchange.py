crypto_currency_to_stars_ratios = {
    "TON": 100
}

def exchange_crypto_to_tg_stars(
        crypto_name: str,
        crypto_amount: float
) -> int | float | None:
    ratio = crypto_currency_to_stars_ratios.get(crypto_name, -1)
    if ratio == -1:
        return None

    stars_amount = crypto_amount * ratio
    return stars_amount
