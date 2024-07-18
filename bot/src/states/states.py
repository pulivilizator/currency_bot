from aiogram.fsm.state import State, StatesGroup


class MainMenuSG(StatesGroup):
    main_menu = State()

class ExchangeSG(StatesGroup):
    exchange = State()

class RatesSG(StatesGroup):
    rates = State()
