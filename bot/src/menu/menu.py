from aiogram import Bot
from aiogram.types import BotCommand


async def set_menu(bot: Bot):
    menu = [
        BotCommand(command='/start', description='show main menu message'),
        BotCommand(command='/help', description='show help message'),
        BotCommand(command='/rates', description='show current exchange rates'),
        BotCommand(command='/exchange', description='show exchange rate\n\ne.g. /exchange USD RUB 100')
    ]

    await bot.set_my_commands(menu)
