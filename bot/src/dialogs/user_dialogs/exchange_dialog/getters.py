from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def exchange_getter(dialog_manager: DialogManager,
                          i18n: TranslatorRunner,
                          **kwargs) -> dict[str, tuple | str]:
    return {
        'exchange_message': i18n.exchange.message(),
        'back_to_menu': i18n.back.to_menu(),
    }
