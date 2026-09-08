from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.node import Node
from app.database.models.system import System
from app.database.models.tool import Tool
from app.database.repositories.node import get_node, get_nodes
from app.database.repositories.system import get_systems


CATEGORY_NAMES = {
    "loading": "Гидросистема погрузочного оборудования",
    "steering": "Гидросистема рулевого управления",
    "brakes": "Гидросистема тормозов",
}


async def get_tool_system(
    session: AsyncSession,
    category: str,
) -> System | None:
    category_name = CATEGORY_NAMES.get(category)

    if category_name is None:
        return None

    systems = await get_systems(
        session,
        "tool",
    )

    for system in systems:
        if system.name == category_name:
            return system

    return None


async def get_all_tool_systems(
    session: AsyncSession,
) -> list[System]:
    return await get_systems(
        session,
        "tool",
    )


async def get_all_tool_nodes(
    session: AsyncSession,
) -> list[Node]:
    systems = await get_all_tool_systems(
        session
    )

    all_nodes: list[Node] = []

    for system in systems:
        nodes = await get_nodes(
            session,
            system.id,
        )

        all_nodes.extend(nodes)

    return all_nodes


async def get_all_tools(
    session: AsyncSession,
) -> list[Tool]:
    nodes = await get_all_tool_nodes(
        session
    )

    tools_by_id: dict[int, Tool] = {}

    for node in nodes:
        for tool in node.tools:
            if tool.is_active:
                tools_by_id[tool.id] = tool

    return sorted(
        tools_by_id.values(),
        key=lambda tool: (
            tool.sort_order,
            tool.id,
        ),
    )


async def get_tools_for_nodes(
    session: AsyncSession,
    node_ids: Sequence[int],
) -> list[Tool]:
    tools_by_id: dict[int, Tool] = {}

    for node_id in node_ids:
        node = await get_node(
            session,
            int(node_id),
        )

        if node is None or not node.is_active:
            continue

        for tool in node.tools:
            if tool.is_active:
                tools_by_id[tool.id] = tool

    return sorted(
        tools_by_id.values(),
        key=lambda tool: (
            tool.sort_order,
            tool.id,
        ),
    )


def format_tools_card(
    title: str,
    tools: Sequence[Tool],
) -> str:
    parts = [
        f"🧰 <b>{title}</b>",
        "",
        "<b>Необходимый инструмент:</b>",
    ]

    for tool in tools:
        parts.append(
            f"\n🔧 <b>{tool.name}</b>"
        )

        if tool.description:
            parts.append(
                tool.description
            )

    return "\n".join(parts)