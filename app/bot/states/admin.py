from aiogram.fsm.state import State, StatesGroup


class AdminSystemStates(StatesGroup):
    waiting_name = State()
    waiting_sort_order = State()

    editing_name = State()
    editing_sort_order = State()