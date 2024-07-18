from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from bot.src.data_stores import Cache, CacheKeys

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def rates_getter(dialog_manager: DialogManager,
                       cache: Cache,
                       i18n: TranslatorRunner,
                       **kwargs) -> dict:
    currencies_raw = await cache.get_all_hkey_data(CacheKeys.Currency.currencies())
    currencies = [(currency_name, currency_value)
                  for currency_name, currency_value in currencies_raw.items()]

    return {
        'rates_message': i18n.rates_message(),
        'currencies': currencies,
        'back_to_menu': i18n.back.to_menu()
    }
