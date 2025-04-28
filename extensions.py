import requests


class APIException(Exception):
    pass


class CurrencyConverter:

    currencies = {
        'евро': 'EUR',
        'доллар': 'USD',
        'рубль': 'RUB'
    }

    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base = base.lower()
        quote = quote.lower()

        if base not in CurrencyConverter.currencies:
            raise APIException(f'Неизвестная валюта {base}')
        if quote not in CurrencyConverter.currencies:
            raise APIException(f'Неизвестная валюта {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Количество должно быть числом.')

        if amount <= 0:
            raise APIException('Количество должно быть положительным числом.')

        base_ticker = CurrencyConverter.currencies[base]
        quote_ticker = CurrencyConverter.currencies[quote]

        url = f'https://api.exchangerate.host/latest?base={base_ticker}&symbols={quote_ticker}'
        response = requests.get(url)
        if response.status_code != 200:
            raise APIException('Ошибка получения данных от API.')

        data = response.json()
        if 'rates' not in data or quote_ticker not in data['rates']:
            raise APIException('Ошибка обработки данных от API.')

        rate = data['rates'][quote_ticker]
        total = rate * amount
        return round(total, 4)