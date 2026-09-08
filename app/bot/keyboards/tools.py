from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.database.models.node import Node


def tools_categories_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="🔧 Гидросистема погрузочного оборудования",
                callback_data="tools:category:loading",
            )
        ],
        [
            InlineKeyboardButton(
                text="🚜 Гидросистема рулевого управления",
                callback_data="tools:category:steering",
            )
        ],
        [
            InlineKeyboardButton(
                text="🛑 Гидросистема тормозов",
                callback_data="tools:category:brakes",
            )
        ],
        [
            InlineKeyboardButton(
                text="⚙️ Узлы",
                callback_data="tools:category:nodes",
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Все",
                callback_data="tools:category:all",
            )
        ],
        [
            InlineKeyboardButton(
                text="🏠 В меню",
                callback_data="menu:main",
            )
        ],
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def nodes_keyboard(
    nodes: list[Node],
) -> InlineKeyboardMarkup:
    buttons = []

    for node in nodes:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=node.name,
                    callback_data=f"tools:node:{node.id}",
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="tools:back:categories",
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


def nodes_selection_keyboard(
    nodes: list[Node],
    selected_ids: set[int],
) -> InlineKeyboardMarkup:
    buttons = []

    for node in nodes:
        selected = node.id in selected_ids
        prefix = "☑️" if selected else "⬜"

        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{prefix} {node.name}",
                    callback_data=f"tools:select_node:{node.id}",
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="✅ ОК",
                callback_data="tools:nodes:confirm",
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="tools:back:categories",
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


def tool_card_keyboard(
    back_callback: str = "tools:back:categories",
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=back_callback,
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


def node_card_keyboard(
    system_id: int,
) -> InlineKeyboardMarkup:
    return tool_card_keyboard(
        back_callback=f"tools:back:nodes:{system_id}"
    )