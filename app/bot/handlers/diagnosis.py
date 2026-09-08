from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.diagnosis import (
    cause_card_keyboard,
    diagnosis_causes_keyboard,
    diagnosis_problems_keyboard,
    diagnosis_systems_keyboard,
)
from app.bot.states.diagnosis import DiagnosisStates
from app.database.repositories.cause import get_causes, get_cause
from app.database.repositories.problem import (
    get_problem,
    get_problems,
)
from app.database.repositories.system import get_system, get_systems
from app.services.cards import format_cause_card


router = Router()


@router.callback_query(
    lambda callback: callback.data == "menu:diagnosis"
)
async def open_diagnosis(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    await state.clear()

    systems = await get_systems(
        session,
        "diagnosis",
    )

    if not systems:
        await callback.message.edit_text(
            "🔧 <b>Диагностика</b>\n\n"
            "Раздел пока не заполнен.",
        )
        await callback.answer()
        return

    await state.set_state(DiagnosisStates.system)

    await callback.message.edit_text(
        "🔧 <b>Диагностика</b>\n\n"
        "Выберите систему:",
        reply_markup=diagnosis_systems_keyboard(systems),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: (
        callback.data is not None
        and callback.data.startswith("diagnosis:system:")
    )
)
async def select_diagnosis_system(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    system_id = int(callback.data.split(":")[-1])

    system = await get_system(
        session,
        system_id,
    )

    if system is None or not system.is_active:
        await callback.answer(
            "Система не найдена.",
            show_alert=True,
        )
        return

    problems = await get_problems(
        session,
        system_id,
    )

    if not problems:
        await callback.message.edit_text(
            f"🔧 <b>{system.name}</b>\n\n"
            "Для этой системы пока нет проблем.",
        )
        await callback.answer()
        return

    await state.update_data(
        system_id=system_id,
        system_name=system.name,
    )

    await state.set_state(DiagnosisStates.problem)

    await callback.message.edit_text(
        f"🔧 <b>{system.name}</b>\n\n"
        "Выберите проблему:",
        reply_markup=diagnosis_problems_keyboard(problems),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: (
        callback.data is not None
        and callback.data.startswith("diagnosis:problem:")
    )
)
async def select_diagnosis_problem(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    problem_id = int(callback.data.split(":")[-1])

    problem = await get_problem(
        session,
        problem_id,
    )

    if problem is None or not problem.is_active:
        await callback.answer(
            "Проблема не найдена.",
            show_alert=True,
        )
        return

    causes = await get_causes(
        session,
        problem_id,
    )

    if not causes:
        await callback.message.edit_text(
            f"⚠️ <b>{problem.name}</b>\n\n"
            "Вероятные причины пока не добавлены.",
        )
        await callback.answer()
        return

    await state.update_data(
        problem_id=problem_id,
        problem_name=problem.name,
    )

    await state.set_state(DiagnosisStates.cause)

    await callback.message.edit_text(
        f"⚠️ <b>{problem.name}</b>\n\n"
        "Выберите вероятную причину:",
        reply_markup=diagnosis_causes_keyboard(causes),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: (
        callback.data is not None
        and callback.data.startswith("diagnosis:cause:")
    )
)
async def open_cause_card(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    cause_id = int(callback.data.split(":")[-1])

    cause = await get_cause(
        session,
        cause_id,
    )

    if cause is None or not cause.is_active:
        await callback.answer(
            "Причина не найдена.",
            show_alert=True,
        )
        return

    await state.update_data(
        cause_id=cause_id,
        cause_name=cause.name,
    )

    text = format_cause_card(cause)

    images = []

    if cause.card:
        images = cause.card.images

    for image in images:
        await callback.message.answer_photo(
            photo=image.telegram_file_id,
            caption=image.caption,
        )

    await callback.message.edit_text(
        text,
        reply_markup=cause_card_keyboard(),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data == "diagnosis:back:systems"
)
async def back_to_systems(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    systems = await get_systems(
        session,
        "diagnosis",
    )

    await state.set_state(DiagnosisStates.system)

    await callback.message.edit_text(
        "🔧 <b>Диагностика</b>\n\n"
        "Выберите систему:",
        reply_markup=diagnosis_systems_keyboard(systems),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data == "diagnosis:back:problems"
)
async def back_to_problems(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    data = await state.get_data()

    system_id = data.get("system_id")

    if system_id is None:
        await callback.answer(
            "Не удалось определить систему.",
            show_alert=True,
        )
        return

    system = await get_system(
        session,
        system_id,
    )

    if system is None:
        await callback.answer(
            "Система не найдена.",
            show_alert=True,
        )
        return

    problems = await get_problems(
        session,
        system_id,
    )

    await state.set_state(DiagnosisStates.problem)

    await callback.message.edit_text(
        f"🔧 <b>{system.name}</b>\n\n"
        "Выберите проблему:",
        reply_markup=diagnosis_problems_keyboard(problems),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data == "diagnosis:back:causes"
)
async def back_to_causes(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    data = await state.get_data()

    problem_id = data.get("problem_id")

    if problem_id is None:
        await callback.answer(
            "Не удалось определить проблему.",
            show_alert=True,
        )
        return

    problem = await get_problem(
        session,
        problem_id,
    )

    if problem is None:
        await callback.answer(
            "Проблема не найдена.",
            show_alert=True,
        )
        return

    causes = await get_causes(
        session,
        problem_id,
    )

    await state.set_state(DiagnosisStates.cause)

    await callback.message.edit_text(
        f"⚠️ <b>{problem.name}</b>\n\n"
        "Выберите вероятную причину:",
        reply_markup=diagnosis_causes_keyboard(causes),
    )

    await callback.answer()