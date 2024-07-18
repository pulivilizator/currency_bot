from .main_menu_dialog import main_menu_dialog
from .exchange_dialog import exchange_dialog
from .rates_dialog import rates_dialog


def get_user_dialog_routers():
    return [main_menu_dialog, rates_dialog, exchange_dialog]
