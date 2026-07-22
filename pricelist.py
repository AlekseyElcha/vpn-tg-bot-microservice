class PaymentsPricesInfo:
     # TODO: в будущем брать из окружение -> настройки -> сюда.
     #  а лучше настроить задачу автообновления ценника с сервера раз в n время

    payment_tariffs_dict: dict[str, int] = {
        "Оплата услуг - 60 stars": 1,
        "Оплата услуг - 120 stars": 2,
        "Оплата услуг - 240 stars": 3,
    }

    daily_service_price: float = 1

    @classmethod
    def associate_tariff_name_and_price(cls, tariff_name: str) -> float| None:

        price = cls.payment_tariffs_dict.get(tariff_name, None)

        return price

