from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.database.models.cause import Cause
from app.database.models.problem import Problem
from app.database.models.system import System


def diagnosis_systems_keyboard(
    systems: list[System],
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=system.name,
                callback_data=f"diagnosis:system:{system.id}",
            )
        ]
        for system in systems
    ]

    buttons.append(
        [
            InlineKeyboardButton(
                text="🏠 В меню",
                callback_data="menu:main",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )


def diagnosis_problems_keyboard(
    problems: list[Problem],
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=problem.name,
                callback_data=f"diagnosis:problem:{problem.id}",
            )
        ]
        for problem in problems
    ]

    buttons.extend(
        [
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="diagnosis:back:systems",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 В меню",
                    callback_data="menu:main",
                )
            ],
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )


def diagnosis_causes_keyboard(
    causes: list[Cause],
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=cause.name,
                callback_data=f"diagnosis:cause:{cause.id}",
            )
        ]
        for cause in causes
    ]

    buttons.extend(
        [
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="diagnosis:back:problems",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 В меню",
                    callback_data="menu:main",
                )
            ],
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )


def cause_card_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="diagnosis:back:causes",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🏠 В меню",
                    callback_data="menu:main",
                ),
            ],
        ]
    )