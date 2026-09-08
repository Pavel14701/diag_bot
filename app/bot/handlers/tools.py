from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.tools import (
    node_card_keyboard,
    nodes_keyboard,
    nodes_selection_keyboard,
    tool_card_keyboard,
    tools_categories_keyboard,
)
from app.bot.states.tools import ToolsStates
from app.database.repositories.node import get_node, get_nodes
from app.database.repositories.system import get_system
from app.services.tools import (
    format_tools_card,
    get_all_tool_nodes,
    get_all_tools,
    get_tool_system,
    get_tools_for_nodes,
)


router = Router()


@router.callback_query(
    lambda callback: callback.data == "menu:tools"
)
async def open_tools(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.clear()

    await callback.message.edit_text(
        "🧰 <b>Инструмент</b>\n\n"
        "Выберите категорию:",
        reply_markup=tools_categories_keyboard(),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data.startswith("tools:category:")
)
async def select_tools_category(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    category = callback.data.split(":")[-1]

    if category == "nodes":
        await open_nodes_selection(
            callback,
            state,
            session,
        )
        return

    if category == "all":
        await open_all_tools(
            callback,
            session,
        )
        return

    system = await get_tool_system(
        session,
        category,
    )

    if system is None:
        await callback.answer(
            "Категория пока не заполнена.",
            show_alert=True,
        )
        return

    nodes = await get_nodes(
        session,
        system.id,
    )

    if not nodes:
        await callback.message.edit_text(
            f"🧰 <b>{system.name}</b>\n\n"
            "В этой категории пока нет узлов.",
            reply_markup=tool_card_keyboard(),
        )

        await callback.answer()
        return

    await callback.message.edit_text(
        f"🧰 <b>{system.name}</b>\n\n"
        "Выберите узел:",
        reply_markup=nodes_keyboard(nodes),
    )

    await callback.answer()


async def open_all_tools(
    callback: CallbackQuery,
    session: AsyncSession,
) -> None:
    tools = await get_all_tools(
        session,
    )

    if not tools:
        await callback.message.edit_text(
            "🧰 <b>Все инструменты</b>\n\n"
            "Инструменты пока не добавлены.",
            reply_markup=tool_card_keyboard(),
        )

        await callback.answer()
        return

    text = [
        "🧰 <b>Все инструменты</b>",
        "",
    ]

    for index, tool in enumerate(tools, start=1):
        text.append(
            f"{index}. <b>{tool.name}</b>"
        )

        if tool.description:
            text.append(
                f"   {tool.description}"
            )

        text.append("")

    await callback.message.edit_text(
        "\n".join(text),
        reply_markup=tool_card_keyboard(),
    )

    await callback.answer()


async def open_nodes_selection(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    nodes = await get_all_tool_nodes(
        session,
    )

    if not nodes:
        await callback.message.edit_text(
            "⚙️ <b>Узлы</b>\n\n"
            "Узлы пока не добавлены.",
            reply_markup=tool_card_keyboard(),
        )

        await callback.answer()
        return

    await state.set_state(
        ToolsStates.selecting_nodes
    )

    await state.update_data(
        selected_node_ids=[]
    )

    await callback.message.edit_text(
        "⚙️ <b>Выбор узлов</b>\n\n"
        "Выберите один или несколько узлов:",
        reply_markup=nodes_selection_keyboard(
            nodes,
            set(),
        ),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data.startswith(
        "tools:select_node:"
    )
)
async def toggle_node_selection(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    node_id = int(
        callback.data.split(":")[-1]
    )

    node = await get_node(
        session,
        node_id,
    )

    if node is None or not node.is_active:
        await callback.answer(
            "Узел не найден.",
            show_alert=True,
        )
        return

    data = await state.get_data()

    selected_ids = set(
        data.get(
            "selected_node_ids",
            [],
        )
    )

    if node_id in selected_ids:
        selected_ids.remove(node_id)
    else:
        selected_ids.add(node_id)

    await state.update_data(
        selected_node_ids=list(selected_ids)
    )

    nodes = await get_all_tool_nodes(
        session,
    )

    await callback.message.edit_reply_markup(
        reply_markup=nodes_selection_keyboard(
            nodes,
            selected_ids,
        )
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data == "tools:nodes:confirm"
)
async def confirm_nodes_selection(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    data = await state.get_data()

    selected_ids = data.get(
        "selected_node_ids",
        [],
    )

    if not selected_ids:
        await callback.answer(
            "Выберите хотя бы один узел.",
            show_alert=True,
        )
        return

    tools = await get_tools_for_nodes(
        session,
        selected_ids,
    )

    if not tools:
        await callback.message.edit_text(
            "⚙️ <b>Результат</b>\n\n"
            "Для выбранных узлов инструмент пока "
            "не назначен.",
            reply_markup=tool_card_keyboard(
                back_callback="tools:category:nodes"
            ),
        )

        await state.clear()
        await callback.answer()
        return

    text = format_tools_card(
        "Инструмент для выбранных узлов",
        tools,
    )

    await callback.message.edit_text(
        text,
        reply_markup=tool_card_keyboard(
            back_callback="tools:category:nodes"
        ),
    )

    await state.clear()

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data.startswith(
        "tools:node:"
    )
)
async def open_tool_node(
    callback: CallbackQuery,
    session: AsyncSession,
) -> None:
    node_id = int(
        callback.data.split(":")[-1]
    )

    node = await get_node(
        session,
        node_id,
    )

    if node is None or not node.is_active:
        await callback.answer(
            "Узел не найден.",
            show_alert=True,
        )
        return

    tools = [
        tool
        for tool in node.tools
        if tool.is_active
    ]

    text = format_tools_card(
        node.name,
        tools,
    )

    await callback.message.edit_text(
        text,
        reply_markup=node_card_keyboard(
            node.system_id
        ),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data.startswith(
        "tools:back:nodes:"
    )
)
async def back_to_nodes(
    callback: CallbackQuery,
    session: AsyncSession,
) -> None:
    system_id = int(
        callback.data.split(":")[-1]
    )

    system = await get_system(
        session,
        system_id,
    )

    if system is None or not system.is_active:
        await callback.answer(
            "Категория не найдена.",
            show_alert=True,
        )
        return

    nodes = await get_nodes(
        session,
        system.id,
    )

    if not nodes:
        await callback.message.edit_text(
            f"🧰 <b>{system.name}</b>\n\n"
            "В этой категории пока нет узлов.",
            reply_markup=tool_card_keyboard(),
        )

        await callback.answer()
        return

    await callback.message.edit_text(
        f"🧰 <b>{system.name}</b>\n\n"
        "Выберите узел:",
        reply_markup=nodes_keyboard(nodes),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data == "tools:back:categories"
)
async def back_to_tools_categories(
    callback: CallbackQuery,
) -> None:
    await callback.message.edit_text(
        "🧰 <b>Инструмент</b>\n\n"
        "Выберите категорию:",
        reply_markup=tools_categories_keyboard(),
    )

    await callback.answer()