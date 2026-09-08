from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="🔧 Диагностика",
                callback_data="menu:diagnosis",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🧰 Инструмент",
                callback_data="menu:tools",
            ),
        ],
    ]

    if is_admin:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="⚙️ Админка",
                    callback_data="menu:admin",
                ),
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)