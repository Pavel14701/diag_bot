from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🩺 Диагностика",
                    callback_data="admin:diagnosis",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧰 Инструменты",
                    callback_data="admin:tools",
                )
            ],
            [
                InlineKeyboardButton(
                    text="👥 Пользователи",
                    callback_data="admin:users",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="menu:main",
                )
            ],
        ]
    )


def admin_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ В админку",
                    callback_data="menu:admin",
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

def admin_diagnosis_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗂 Системы",
                    callback_data="admin:diagnosis:systems",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔴 Проблемы",
                    callback_data="admin:diagnosis:problems",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚠️ Причины",
                    callback_data="admin:diagnosis:causes",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Карточки",
                    callback_data="admin:diagnosis:cards",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ В админку",
                    callback_data="menu:admin",
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

def admin_systems_keyboard(
    systems,
) -> InlineKeyboardMarkup:
    buttons = []

    for system in systems:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"🗂 {system.name}",
                    callback_data=f"admin:system:{system.id}",
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="➕ Добавить систему",
                callback_data="admin:system:add",
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="🗑 Отключённые системы",
                callback_data="admin:systems:inactive",
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="admin:diagnosis",
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="🏠 В меню",
                callback_data="menu:main",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

def admin_system_card_keyboard(
    system_id: int,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Изменить",
                    callback_data=f"admin:system:edit:{system_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⛔ Отключить",
                    callback_data=f"admin:system:deactivate:{system_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔴 Проблемы",
                    callback_data=f"admin:system:problems:{system_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="admin:diagnosis:systems",
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

def admin_inactive_systems_keyboard(systems) -> InlineKeyboardMarkup:
    buttons = []

    for system in systems:
        buttons.append([
            InlineKeyboardButton(
                text=f"🗑 {system.name}",
                callback_data=f"admin:inactive_system:{system.id}",
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="admin:diagnosis:systems",
        )
    ])

    buttons.append([
        InlineKeyboardButton(
            text="🏠 В меню",
            callback_data="menu:main",
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

def admin_inactive_system_card_keyboard(
    system_id: int,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="♻️ Восстановить",
                    callback_data=f"admin:system:restore:{system_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Удалить окончательно",
                    callback_data=f"admin:system:delete:{system_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="admin:systems:inactive",
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

def admin_delete_system_confirm_keyboard(
    system_id: int,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Да, удалить окончательно",
                    callback_data=f"admin:system:delete_confirm:{system_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Отмена",
                    callback_data=f"admin:inactive_system:{system_id}",
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