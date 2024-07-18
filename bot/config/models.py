from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class AioRedis:
    host: str
    port: int


@dataclass
class Nats:
    servers: list[str]
