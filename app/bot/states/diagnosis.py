from aiogram.fsm.state import State, StatesGroup


class DiagnosisStates(StatesGroup):
    system = State()
    problem = State()
    cause = State()