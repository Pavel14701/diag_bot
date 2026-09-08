from aiogram.fsm.state import State, StatesGroup


class ToolsStates(StatesGroup):
    selecting_nodes = State()