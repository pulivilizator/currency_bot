from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Format

from .getters import exchange_getter
from .handlers import incorrect_message_handler, correct_parameters_handler, incorrect_text_handler
from .filters import exchange_filter
from bot.src.states import ExchangeSG

exchange_dialog = Dialog(
    Window(
        Format('{exchange_message}'),
        TextInput(
            id='exchange',
            type_factory=exchange_filter,
            on_success=correct_parameters_handler,
            on_error=incorrect_text_handler
        ),
        MessageInput(
            func=incorrect_message_handler,
            content_types=ContentType.ANY
        ),
        Cancel(text=Format('{back_to_menu}'),
               id='to_menu'),
        state=ExchangeSG.exchange,
        getter=exchange_getter
    ),
)