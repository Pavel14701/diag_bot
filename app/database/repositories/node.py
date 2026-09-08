from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models.node import Node


async def get_nodes(
    session: AsyncSession,
    system_id: int,
) -> list[Node]:
    result = await session.scalars(
        select(Node)
        .options(
            selectinload(Node.tools)
        )
        .where(
            Node.system_id == system_id,
            Node.is_active.is_(True),
        )
        .order_by(Node.sort_order, Node.id)
    )

    return list(result.all())


async def get_node(
    session: AsyncSession,
    node_id: int,
) -> Node | None:
    result = await session.scalar(
        select(Node)
        .options(
            selectinload(Node.tools)
        )
        .where(Node.id == node_id)
    )

    return result