from typing import Sequence


class KeysConverter:
    def __init__(self, *args: Sequence):
        self._keys: list = list(args)

    def __getattr__(self, item):
        return self.__class__(*(self._keys + [item]))

    def __str__(self, id=False):
        if not id:
            return ':'.join(self._keys)
        return '_'.join(self._keys)


class CacheKeys:
    class Settings:
        @staticmethod
        def language(key_to_id=False) -> str:
            return KeysConverter('settings', 'language').__str__(id=key_to_id)

    class Currency:
        @staticmethod
        def current(current, key_to_id=False) -> str:
            return KeysConverter('currency', current).__str__(id=key_to_id)

        @staticmethod
        def currencies() -> str:
            return 'currencies'

    class Exchange:
        ...
