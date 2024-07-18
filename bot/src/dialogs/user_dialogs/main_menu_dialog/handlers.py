from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedRadio

from bot.src.data_stores import Cache, CacheKeys


async def change_lang_handler(callback: CallbackQuery,
                              widget: ManagedRadio,
                              dialog_manager: DialogManager,
                              item_id: str):
    cache: Cache = dialog_manager.middleware_data.get('cache')

    await cache.set_user_data(user_id=callback.from_user.id, key=CacheKeys.Settings.language(), value=item_id)