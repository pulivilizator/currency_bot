from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Radio, Start
from aiogram_dialog.widgets.text import Format

from bot.src.data_stores import CacheKeys
from bot.src.setters import SetButtonChecked
from bot.src.states.states import MainMenuSG, ExchangeSG, RatesSG
from .getters import get_langs, main_menu_getter
from .handlers import change_lang_handler

main_menu_dialog = Dialog(
    Window(
        Format('{main_menu_message}'),
        Start(Format('{start_exchange}'), state=ExchangeSG.exchange, id='start_exchange'),
        Start(Format('{start_rates}'), state=RatesSG.rates, id='start_rates'),
        Row(
            Radio(
                checked_text=Format('🔘 {item[1]}'),
                unchecked_text=Format('⚪️ {item[1]}'),
                id=CacheKeys.Settings.language(key_to_id=True),
                item_id_getter=lambda x: x[0],
                on_state_changed=change_lang_handler,
                items='languages',
            ),
        ),
        getter=get_langs,
        state=MainMenuSG.main_menu,
    ),
    on_start=SetButtonChecked(CacheKeys.Settings.language),
    getter=main_menu_getter
)