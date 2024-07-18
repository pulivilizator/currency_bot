from decimal import Decimal

from bot.src.data_stores import Cache, CacheKeys


async def _get_currency_rate(currency_name: str, cache: Cache) -> Decimal:
    rate = await cache.get_value(key=currency_name, hkey=CacheKeys.Currency.currencies())

    if rate is None:
        raise ValueError(f"Валюта {currency_name} не найдена")
    return Decimal(rate.replace(',', '.'))


async def convert_currency(amount, from_currency, to_currency, cache: Cache):
    if from_currency == to_currency:
        return amount
    if to_currency == 'RUB':
        from_rate = await _get_currency_rate(from_currency, cache=cache)
        return from_rate * Decimal(amount)
    if from_currency == 'RUB':
        to_rate = await _get_currency_rate(to_currency, cache=cache)
        return Decimal(amount) / to_rate
    from_rate = await _get_currency_rate(from_currency, cache=cache)
    to_rate = await _get_currency_rate(to_currency, cache=cache)

    amount_in_rub = Decimal(amount) * from_rate
    converted_amount = amount_in_rub / to_rate

    return converted_amount

