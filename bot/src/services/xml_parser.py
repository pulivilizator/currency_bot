import asyncio
import xml.etree.ElementTree as ET

from aiogram.client.session.aiohttp import AiohttpSession

from bot.src.data_stores import Cache, CacheKeys


async def parse_xml(session: AiohttpSession, cache: Cache = None):
    client = await session.create_session()
    async with client.get('https://cbr.ru/scripts/XML_daily.asp') as response:
        content = await response.read()
    currencies = await asyncio.to_thread(_get_currencies, content)
    await cache.set_currency_data(key=CacheKeys.Currency.currencies(), mapping_values=currencies)


def _get_currencies(content: bytes) -> dict[str, str]:
    root = ET.fromstring(content)
    currencies = {currency.find('CharCode').text: currency.find('Value').text
                  for currency in root.findall('Valute')}
    return currencies
