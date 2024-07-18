from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from fluentogram import TranslatorRunner

from bot.src.data_stores import Cache
from bot.src.states import RatesSG, MainMenuSG, ExchangeSG
from bot.src.services.currency_converter import convert_currency
from bot.src.dialogs.user_dialogs.exchange_dialog.filters import exchange_filter

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

commands_router = Router()


@commands_router.message(CommandStart())
async def process_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=MainMenuSG.main_menu, mode=StartMode.RESET_STACK)


@commands_router.message(Command('rates'))
async def process_rates(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=RatesSG.rates, mode=StartMode.RESET_STACK, show_mode=ShowMode.EDIT)


@commands_router.message(Command('exchange'))
async def process_exchange(message: Message,
                           dialog_manager: DialogManager,
                           cache: Cache,
                           i18n: TranslatorRunner):
    try:
        text = exchange_filter(' '.join(message.text.split(' ')[1:]))
    except ValueError:
        await message.answer(i18n.exchange.err.message())
        return

    text = text.strip().split(' ')
    from_currency = text[0]
    to_currency = text[1]
    amount = text[2]
    result = await convert_currency(from_currency=from_currency,
                                    to_currency=to_currency,
                                    amount=amount,
                                    cache=cache)
    await message.answer(f'{amount} {from_currency} = {result} {to_currency}')
    await dialog_manager.start(state=ExchangeSG.exchange, mode=StartMode.RESET_STACK)


@commands_router.message(Command('help'))
async def process_help(message: Message,
                       dialog_manager: DialogManager,
                       i18n: TranslatorRunner):
    await message.answer(i18n.help.message())
    await dialog_manager.start(state=MainMenuSG.main_menu, mode=StartMode.RESET_STACK)
