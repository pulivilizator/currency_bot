import asyncio

from aiogram.client.session.aiohttp import AiohttpSession
from redis.asyncio import Redis
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker

from bot.config import get_config
from bot.src.data_stores import Cache, CacheKeys
from bot.src.services.xml_parser import _get_currencies

config = get_config()

broker = NatsBroker(
    config.nats.servers,
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


@broker.task(broker.task(
    schedule=[
        {
            "cron": "0 0 * * *",
            "args": [],
            "kwargs": {},
            "labels": {},
        }
    ]
))
async def parse_xml():
    r = Redis(host=config.redis.host, port=config.redis.port)
    session = AiohttpSession()
    cache = Cache(r)
    try:
        client = await session.create_session()
        async with client.get('https://cbr.ru/scripts/XML_daily.asp') as response:
            content = await response.read()
    finally:
        await session.close()
        await r.close()
    currencies = await asyncio.to_thread(_get_currencies, content)
    await cache.set_currency_data(key=CacheKeys.Currency.currencies(), mapping_values=currencies)
