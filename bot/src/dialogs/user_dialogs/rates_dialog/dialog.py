from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, ListGroup, Button, Cancel, Start
from aiogram_dialog.widgets.text import Format

from bot.src.dialogs.kbd import get_scroll_buttons
from bot.src.states import RatesSG, MainMenuSG

from .getters import rates_getter

rates_dialog = Dialog(
    Window(
        Format('{rates_message}'),
        ScrollingGroup(
            ListGroup(Button(text=Format('{item[0]} - {item[1]} Rub'), id='currency'),
                      items='currencies',
                      id='currency_list',
                      item_id_getter=lambda x: x[0]),
            id='currencies',
            width=1,
            height=5,
            hide_pager=True
        ),
        get_scroll_buttons(scroll_id='currencies', when=None),
        Start(text=Format('{back_to_menu}'),
              state=MainMenuSG.main_menu,
              id='to_menu'),
        state=RatesSG.rates,
        getter=rates_getter
    )
)
