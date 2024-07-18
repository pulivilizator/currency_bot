from .user_dialogs import get_user_dialog_routers


def get_dialog_routers():
    return [*get_user_dialog_routers()]