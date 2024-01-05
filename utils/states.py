from aiogram.fsm.state import StatesGroup, State


class CheckAdmin(StatesGroup):
    password = State()

class CryproBot(StatesGroup):
    sum = State()
    currency = State()

class ConfigState(StatesGroup):
    mailing = State()
    setPrice = State()