from typing import TYPE_CHECKING

from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput, ManagedTextInput
from fluentogram import TranslatorRunner

from bot.src.data_stores import Cache
from bot.src.services import convert_currency

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def incorrect_message_handler(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await message.answer(i18n.exchange.err.message())


async def correct_parameters_handler(message: Message,
                                     widget: ManagedTextInput,
                                     dialog_manager: DialogManager,
                                     text: str):
    currencies = text.strip().split(' ')
    from_currency = currencies[0]
    to_currency = currencies[1]
    amount = currencies[2]
    cache: Cache = dialog_manager.middleware_data.get('cache')
    result_currency = await convert_currency(amount=amount,
                                             from_currency=from_currency,
                                             to_currency=to_currency,
                                             cache=cache)
    await message.answer(f'{amount} {from_currency} = {result_currency} {to_currency}')


async def incorrect_text_handler(message: Message,
                                 widget: ManagedTextInput | MessageInput,
                                 dialog_manager: DialogManager,
                                 err: Exception | None = None):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await message.answer(i18n.exchange.err.message())
