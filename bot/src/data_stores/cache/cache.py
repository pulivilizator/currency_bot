import asyncio
import logging
from typing import TypeAlias, Optional

from redis.asyncio import Redis

KeyType: TypeAlias = Optional[str]
ValueType: TypeAlias = Optional[str | bool | int]
MappingValuesType: TypeAlias = Optional[dict[KeyType, ValueType]]

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self, r: Redis):
        self._r = r

    async def set_data(self, key: KeyType = None,
                       value: ValueType = None,
                       mapping_values: MappingValuesType = None):
        logger.info(f'set key: {key}, value: {value}, mapping_values: {mapping_values}')
        if mapping_values:
            await asyncio.gather(*[
                self._r.set(name=name, value=value)
                for name, value in mapping_values.items()
            ])
            return
        await self._r.set(name=str(key), value=str(value))

    async def set_currency_data(self,
                                key: KeyType,
                                mapping_values: MappingValuesType = None):
        logger.info(f'set key: {key}, mapping_values: {mapping_values}')
        await self._r.hset(name='currencies', mapping=mapping_values)

    async def set_user_data(self, user_id: int,
                            key: KeyType = None,
                            value: ValueType = None,
                            mapping_values: MappingValuesType = None) -> None:
        logger.info(f'{user_id}: set data for key: {key}')

        user_key = str(user_id)
        if mapping_values:
            set_data = {k: str(v)
            if not isinstance(v, bool)
            else '0'
            if not v
            else '1'
                        for k, v in mapping_values.items()}
            await self._r.hset(name=user_key, mapping=set_data)
        else:
            if isinstance(value, bool):
                value = int(value)
            await self._r.hset(name=user_key, key=str(key), value=str(value))

    async def get_value(self, key: KeyType,
                        hkey: int | str | None = None) -> ValueType:
        if hkey:
            bytes_value: Optional[bytes] = await self._r.hget(name=str(hkey), key=str(key))
            logger.info(f'{hkey}: get value')
        else:
            bytes_value: Optional[bytes] = await self._r.get(name=str(key))
            logger.info(f'{key}: get value')

        if not bytes_value:
            return
        user_value = bytes_value.decode('utf-8-sig')

        return int(user_value) if user_value.isdigit() else user_value

    async def get_all_hkey_data(self, hkey: int | str) -> MappingValuesType:
        user_bytes_data: Optional[dict[bytes, bytes]] = await self._r.hgetall(name=hkey)
        logger.info(f'{hkey} get all values')

        if not user_bytes_data:
            return

        mapping_values = {key.decode('utf-8-sig'): int(value.decode('utf-8-sig'))
                          if value.isdigit() else value.decode('utf-8-sig')
                          for key, value in user_bytes_data.items()}

        return mapping_values

    async def user_exists(self, user_id: int) -> bool:
        user_key = str(user_id)
        return await self._r.exists(user_key)
