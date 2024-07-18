from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram_dialog import setup_dialogs
from nats.aio.client import Client as NATSClient
from nats.js import JetStreamContext

from redis.asyncio import Redis

import asyncio
import logging

from .config import get_config
from .src import get_routers
from .storage import NatsStorage
from .src.utils import connect_to_nats, create_translator_hub
from .src.middlewares import TranslatorRunnerMiddleware, CacheMiddleware
from .src.menu import set_menu
from .src.data_stores.cache import Cache
from .src.tkq.tkq import broker, parse_xml

logging.basicConfig(level=logging.DEBUG,
                    format='[#{levelname} - {asctime}]\n{filename} - {name}|{funcName} - {lineno}: {message}\n',
                    style='{')


async def main():
    config = get_config()
    nc, js = await connect_to_nats(config.nats.servers)
    session = AiohttpSession()
    r = Redis(host=config.redis.host, port=config.redis.port)
    cache = Cache(r)
    dp = await create_dispatcher(nc=nc,
                                 js=js,
                                 session=session,
                                 cache=cache)
    await broker.startup()
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await parse_xml(session, cache)
    try:
        await dp.start_polling(bot)
    finally:
        await broker.shutdown()
        await nc.close()
        await session.close()
        await r.aclose()


async def create_dispatcher(nc: NATSClient,
                            js: JetStreamContext,
                            session: AiohttpSession,
                            cache: Cache) -> Dispatcher:
    storage = await NatsStorage(nc=nc, js=js).create_storage()
    dp = Dispatcher(storage=storage)

    hub = create_translator_hub()

    dp.workflow_data.update({'cache': cache,
                             'hub': hub,
                             'aiohttp_session': session,
                             })

    dp.include_routers(*get_routers())
    dp.startup.register(set_menu)
    dp.update.middleware(CacheMiddleware())
    dp.update.middleware(TranslatorRunnerMiddleware())

    return dp


if __name__ == '__main__':
    asyncio.run(main())
