from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from bot.src.utils.enums import Language

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


async def main_menu_getter(dialog_manager: DialogManager,
                           i18n: TranslatorRunner,
                           **kwargs) -> dict[str, tuple | str]:
    return {
        'main_menu_message': i18n.main_menu_message(),
        'start_exchange': i18n.start.exchange(),
        'start_rates': i18n.start.rates(),
    }


async def get_langs(dialog_manager: DialogManager,
                    i18n: TranslatorRunner,
                    **kwargs) -> dict[str, tuple | str]:
    return {
        'languages': (
            (Language.RU.value, i18n.lang.ru()),
            (Language.EN.value, i18n.lang.en())
        ),
        'main': i18n.language.change.message()
    }
