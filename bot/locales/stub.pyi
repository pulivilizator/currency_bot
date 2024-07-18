from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    lang: Lang
    start: Start
    exchange: Exchange
    back: Back
    help: Help

    @staticmethod
    def main_menu_message() -> Literal["""&lt;b&gt;Hi!&lt;/b&gt;.
This is a currency conversion bot and currency rate viewer.
Send /help for more details"""]: ...

    @staticmethod
    def rates_message() -> Literal["""Currency rate"""]: ...


class Lang:
    @staticmethod
    def ru() -> Literal["""🇷🇺 Русский"""]: ...

    @staticmethod
    def en() -> Literal["""🇬🇧 English"""]: ...


class Start:
    @staticmethod
    def exchange() -> Literal["""Currency Converter"""]: ...

    @staticmethod
    def rates() -> Literal["""Currency rate"""]: ...


class Exchange:
    err: ExchangeErr

    @staticmethod
    def message() -> Literal["""Send what currency you want to change in the format &lt;b&gt;&#34;what-convert to-what-convert quantity&#34;&lt;/b&gt;

For example: &lt;b&gt;&#34;USD RUB 100&#34;&lt;/b&gt;"""]: ...


class ExchangeErr:
    @staticmethod
    def message() -> Literal["""Invalid message format"""]: ...


class Back:
    @staticmethod
    def to_menu() -> Literal["""Back to main menu"""]: ...


class Help:
    @staticmethod
    def message() -> Literal["""This bot shows current exchange rates, as well as converts them

/start - go to the main menu
/exchange from to amount - converts the amount of currency from currency from to currency to
/rates - show current exchange rates"""]: ...

