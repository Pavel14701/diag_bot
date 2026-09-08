from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.cause import Cause
from app.database.models.cause_card import CauseCard
from app.database.models.cause_image import CauseImage
from app.database.models.node import Node, node_tools
from app.database.models.problem import Problem
from app.database.models.system import System


async def get_systems(
    session: AsyncSession,
    system_type: str,
) -> list[System]:
    result = await session.scalars(
        select(System)
        .where(
            System.type == system_type,
            System.is_active.is_(True),
        )
        .order_by(
            System.sort_order,
            System.id,
        )
    )

    return list(result.all())


async def get_system(
    session: AsyncSession,
    system_id: int,
) -> System | None:
    return await session.get(
        System,
        system_id,
    )


async def create_system(
    session: AsyncSession,
    name: str,
    system_type: str,
    sort_order: int = 0,
) -> System:
    system = System(
        name=name,
        type=system_type,
        sort_order=sort_order,
        is_active=True,
    )

    session.add(system)

    await session.commit()
    await session.refresh(system)

    return system


async def update_system(
    session: AsyncSession,
    system: System,
    name: str,
    sort_order: int,
) -> System:
    system.name = name
    system.sort_order = sort_order

    await session.commit()
    await session.refresh(system)

    return system


async def deactivate_system(
    session: AsyncSession,
    system: System,
) -> None:
    system.is_active = False

    await session.commit()


async def get_inactive_systems(
    session: AsyncSession,
    system_type: str,
) -> list[System]:
    result = await session.scalars(
        select(System)
        .where(
            System.type == system_type,
            System.is_active.is_(False),
        )
        .order_by(
            System.sort_order,
            System.id,
        )
    )

    return list(result.all())


async def restore_system(
    session: AsyncSession,
    system: System,
) -> System:
    system.is_active = True

    await session.commit()
    await session.refresh(system)

    return system

async def delete_system(
    session: AsyncSession,
    system: System,
) -> None:
    await session.delete(system)
    await session.commit()


async def delete_system(
    session: AsyncSession,
    system: System,
) -> None:
    problems = list(
        await session.scalars(
            select(Problem).where(
                Problem.system_id == system.id
            )
        )
    )

    problem_ids = [problem.id for problem in problems]

    if problem_ids:
        causes = list(
            await session.scalars(
                select(Cause).where(
                    Cause.problem_id.in_(problem_ids)
                )
            )
        )

        cause_ids = [cause.id for cause in causes]

        if cause_ids:
            cards = list(
                await session.scalars(
                    select(CauseCard).where(
                        CauseCard.cause_id.in_(cause_ids)
                    )
                )
            )

            card_ids = [card.id for card in cards]

            if card_ids:
                await session.execute(
                    delete(CauseImage).where(
                        CauseImage.card_id.in_(card_ids)
                    )
                )

                await session.execute(
                    delete(CauseCard).where(
                        CauseCard.id.in_(card_ids)
                    )
                )

            await session.execute(
                delete(Cause).where(
                    Cause.id.in_(cause_ids)
                )
            )

        await session.execute(
            delete(Problem).where(
                Problem.id.in_(problem_ids)
            )
        )

    nodes = list(
        await session.scalars(
            select(Node).where(
                Node.system_id == system.id
            )
        )
    )

    node_ids = [node.id for node in nodes]

    if node_ids:
        await session.execute(
            delete(node_tools).where(
                node_tools.c.node_id.in_(node_ids)
            )
        )

        await session.execute(
            delete(Node).where(
                Node.id.in_(node_ids)
            )
        )

    await session.execute(
        delete(System).where(
            System.id == system.id
        )
    )

    await session.commit()