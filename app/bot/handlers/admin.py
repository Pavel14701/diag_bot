from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.admin import (
    admin_back_keyboard,
    admin_diagnosis_keyboard,
    admin_main_keyboard,
    admin_system_card_keyboard,
    admin_systems_keyboard,
    admin_inactive_system_card_keyboard,
    admin_inactive_systems_keyboard,
    admin_delete_system_confirm_keyboard,
)
from app.bot.states.admin import AdminSystemStates
from app.database.repositories.system import (
    create_system,
    deactivate_system,
    get_system,
    get_systems,
    update_system,
    get_inactive_systems,
    restore_system,
    delete_system,
)
from app.services.admin import is_admin


router = Router()


async def ensure_admin(
    callback: CallbackQuery,
) -> bool:
    user_id = callback.from_user.id

    if not is_admin(user_id):
        await callback.answer(
            "⛔ У вас нет доступа к этому разделу.",
            show_alert=True,
        )
        return False

    return True


@router.callback_query(
    lambda callback: callback.data == "menu:admin"
)
async def open_admin(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not await ensure_admin(callback):
        return

    await state.clear()

    await callback.message.edit_text(
        "⚙️ <b>Админ-панель</b>\n\n"
        "Выберите раздел для управления:",
        reply_markup=admin_main_keyboard(),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data == "admin:diagnosis"
)
async def admin_diagnosis(
    callback: CallbackQuery,
) -> None:
    if not await ensure_admin(callback):
        return

    await callback.message.edit_text(
        "🩺 <b>Управление диагностикой</b>\n\n"
        "Выберите раздел:",
        reply_markup=admin_diagnosis_keyboard(),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data == "admin:tools"
)
async def admin_tools(
    callback: CallbackQuery,
) -> None:
    if not await ensure_admin(callback):
        return

    await callback.message.edit_text(
        "🧰 <b>Управление инструментами</b>\n\n"
        "Раздел пока находится в разработке.",
        reply_markup=admin_back_keyboard(),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data == "admin:users"
)
async def admin_users(
    callback: CallbackQuery,
) -> None:
    if not await ensure_admin(callback):
        return

    await callback.message.edit_text(
        "👥 <b>Пользователи</b>\n\n"
        "Раздел пока находится в разработке.",
        reply_markup=admin_back_keyboard(),
    )

    await callback.answer()

@router.callback_query(
    lambda callback: callback.data == "admin:diagnosis:systems"
)
async def admin_systems(
    callback: CallbackQuery,
    state: FSMContext,
    session,
) -> None:
    if not await ensure_admin(callback):
        return

    await state.clear()

    systems = await get_systems(
        session,
        "diagnosis",
    )

    if not systems:
        await callback.message.edit_text(
            "🗂 <b>Системы диагностики</b>\n\n"
            "Систем пока нет.",
            reply_markup=admin_systems_keyboard(
                systems
            ),
        )

        await callback.answer()
        return

    text = [
        "🗂 <b>Системы диагностики</b>",
        "",
    ]

    for index, system in enumerate(
        systems,
        start=1,
    ):
        text.append(
            f"{index}. {system.name}"
        )

    await callback.message.edit_text(
        "\n".join(text),
        reply_markup=admin_systems_keyboard(
            systems
        ),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data == "admin:systems:inactive"
)
async def admin_inactive_systems(
    callback: CallbackQuery,
    state: FSMContext,
    session,
) -> None:
    if not await ensure_admin(callback):
        return

    await state.clear()

    systems = await get_inactive_systems(
        session,
        "diagnosis",
    )

    if not systems:
        await callback.message.edit_text(
            "🗑 <b>Отключённые системы</b>\n\n"
            "Отключённых систем нет.",
            reply_markup=admin_inactive_systems_keyboard(systems),
        )
        await callback.answer()
        return

    text = [
        "🗑 <b>Отключённые системы</b>",
        "",
    ]

    for index, system in enumerate(systems, start=1):
        text.append(
            f"{index}. {system.name}"
        )

    await callback.message.edit_text(
        "\n".join(text),
        reply_markup=admin_inactive_systems_keyboard(systems),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data.startswith(
        "admin:inactive_system:"
    )
)
async def open_inactive_admin_system(
    callback: CallbackQuery,
    state: FSMContext,
    session,
) -> None:
    if not await ensure_admin(callback):
        return

    system_id = int(
        callback.data.split(":")[-1]
    )

    system = await get_system(
        session,
        system_id,
    )

    if system is None or system.is_active:
        await callback.answer(
            "Система не найдена или уже восстановлена.",
            show_alert=True,
        )
        return

    await state.clear()

    await callback.message.edit_text(
        "🗑 <b>Отключённая система</b>\n\n"
        f"<b>Название:</b> {system.name}\n"
        f"<b>Тип:</b> {system.type}\n"
        f"<b>Порядок:</b> {system.sort_order}\n\n"
        "Система не отображается пользователям.",
        reply_markup=admin_inactive_system_card_keyboard(
            system.id
        ),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data.startswith(
        "admin:system:delete:"
    )
    and not callback.data.startswith(
        "admin:system:delete_confirm:"
    )
)
async def delete_admin_system_warning(
    callback: CallbackQuery,
    state: FSMContext,
    session,
) -> None:
    if not await ensure_admin(callback):
        return

    system_id = int(
        callback.data.split(":")[-1]
    )

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

    if system.is_active:
        await callback.answer(
            "Сначала отключите систему.",
            show_alert=True,
        )
        return

    await state.clear()

    await callback.message.edit_text(
        "⚠️ <b>Окончательное удаление</b>\n\n"
        f"Система:\n"
        f"<b>{system.name}</b>\n\n"
        "После удаления будут потеряны связанные "
        "данные этой системы.\n\n"
        "Это действие нельзя отменить.\n\n"
        "<b>Вы действительно хотите удалить систему?</b>",
        reply_markup=admin_delete_system_confirm_keyboard(
            system.id
        ),
    )

    await callback.answer()


@router.callback_query(
    lambda callback: callback.data.startswith(
        "admin:system:restore:"
    )
)
async def restore_admin_system(
    callback: CallbackQuery,
    state: FSMContext,
    session,
) -> None:
    if not await ensure_admin(callback):
        return

    system_id = int(
        callback.data.split(":")[-1]
    )

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

    if system.is_active:
        await callback.answer(
            "Система уже активна.",
            show_alert=True,
        )
        return

    system = await restore_system(
        session,
        system,
    )

    await state.clear()

    systems = await get_inactive_systems(
        session,
        "diagnosis",
    )

    await callback.message.edit_text(
        "♻️ <b>Система восстановлена</b>\n\n"
        f"<b>{system.name}</b>\n\n"
        "Она снова доступна в разделе диагностики.",
        reply_markup=admin_inactive_systems_keyboard(
            systems
        ),
    )

    await callback.answer()
    

@router.callback_query(
    lambda callback: callback.data == "admin:system:add"
)
async def admin_add_system(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not await ensure_admin(callback):
        return

    await state.set_state(
        AdminSystemStates.waiting_name
    )

    await callback.message.edit_text(
        "➕ <b>Добавление системы</b>\n\n"
        "Введите название системы:",
    )

    await callback.answer()


@router.message(
    AdminSystemStates.waiting_name
)
async def admin_system_name(
    message: Message,
    state: FSMContext,
) -> None:
    if not is_admin(message.from_user.id):
        await message.answer(
            "⛔ У вас нет доступа."
        )
        await state.clear()
        return

    name = message.text.strip()

    if not name:
        await message.answer(
            "Название не может быть пустым.\n\n"
            "Введите название системы:"
        )
        return

    await state.update_data(
        system_name=name
    )

    await state.set_state(
        AdminSystemStates.waiting_sort_order
    )

    await message.answer(
        "Введите порядковый номер системы.\n\n"
        "Например: <code>1</code>"
    )


@router.message(
    AdminSystemStates.waiting_sort_order
)
async def admin_system_sort_order(
    message: Message,
    state: FSMContext,
    session,
) -> None:
    if not is_admin(message.from_user.id):
        await message.answer(
            "⛔ У вас нет доступа."
        )
        await state.clear()
        return

    try:
        sort_order = int(
            message.text.strip()
        )
    except (TypeError, ValueError):
        await message.answer(
            "Введите целое число.\n\n"
            "Например: <code>1</code>"
        )
        return

    data = await state.get_data()

    system = await create_system(
        session=session,
        name=data["system_name"],
        system_type="diagnosis",
        sort_order=sort_order,
    )

    await state.clear()

    systems = await get_systems(
        session,
        "diagnosis",
    )

    text = [
        "✅ <b>Система успешно добавлена!</b>",
        "",
        f"🗂 <b>{system.name}</b>",
        f"Порядок: {system.sort_order}",
        "",
        "Список систем:",
        "",
    ]

    for index, item in enumerate(
        systems,
        start=1,
    ):
        text.append(
            f"{index}. {item.name}"
        )

    await message.answer(
        "\n".join(text),
        reply_markup=admin_systems_keyboard(
            systems
        ),
    )

@router.callback_query(
    lambda callback: callback.data.startswith(
        "admin:system:"
    )
    and callback.data.count(":") == 2
)
async def open_admin_system(
    callback: CallbackQuery,
    state: FSMContext,
    session,
) -> None:
    if not await ensure_admin(callback):
        return

    system_id = int(
        callback.data.split(":")[-1]
    )

    system = await get_system(
        session,
        system_id,
    )

    if system is None or not system.is_active:
        await callback.answer(
            "Система не найдена или отключена.",
            show_alert=True,
        )
        return

    await state.clear()

    await callback.message.edit_text(
        "🗂 <b>Система диагностики</b>\n\n"
        f"<b>Название:</b> {system.name}\n"
        f"<b>Тип:</b> {system.type}\n"
        f"<b>Порядок:</b> {system.sort_order}",
        reply_markup=admin_system_card_keyboard(
            system.id
        ),
    )

    await callback.answer()

@router.callback_query(
    lambda callback: callback.data.startswith(
        "admin:system:edit:"
    )
)
async def edit_admin_system(
    callback: CallbackQuery,
    state: FSMContext,
    session,
) -> None:
    if not await ensure_admin(callback):
        return

    system_id = int(
        callback.data.split(":")[-1]
    )

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

    await state.update_data(
        system_id=system.id,
    )

    await state.set_state(
        AdminSystemStates.editing_name
    )

    await callback.message.edit_text(
        "✏️ <b>Редактирование системы</b>\n\n"
        f"Текущее название:\n"
        f"<b>{system.name}</b>\n\n"
        "Введите новое название:"
    )

    await callback.answer()

@router.message(
    AdminSystemStates.editing_name
)
async def edit_admin_system_name(
    message: Message,
    state: FSMContext,
) -> None:
    if not is_admin(message.from_user.id):
        await message.answer(
            "⛔ У вас нет доступа."
        )
        await state.clear()
        return

    name = (message.text or "").strip()

    if not name:
        await message.answer(
            "Название не может быть пустым.\n\n"
            "Введите новое название:"
        )
        return

    await state.update_data(
        system_name=name,
    )

    await state.set_state(
        AdminSystemStates.editing_sort_order
    )

    await message.answer(
        "Введите новый порядковый номер.\n\n"
        "Например: <code>1</code>"
    )

@router.message(
    AdminSystemStates.editing_sort_order
)
async def edit_admin_system_sort_order(
    message: Message,
    state: FSMContext,
    session,
) -> None:
    if not is_admin(message.from_user.id):
        await message.answer(
            "⛔ У вас нет доступа."
        )
        await state.clear()
        return

    try:
        sort_order = int(
            (message.text or "").strip()
        )
    except ValueError:
        await message.answer(
            "Введите целое число.\n\n"
            "Например: <code>1</code>"
        )
        return

    data = await state.get_data()

    system = await get_system(
        session,
        int(data["system_id"]),
    )

    if system is None or not system.is_active:
        await state.clear()

        await message.answer(
            "❌ Система не найдена."
        )
        return

    system = await update_system(
        session=session,
        system=system,
        name=data["system_name"],
        sort_order=sort_order,
    )

    await state.clear()

    await message.answer(
        "✅ <b>Система изменена</b>\n\n"
        f"<b>Название:</b> {system.name}\n"
        f"<b>Порядок:</b> {system.sort_order}",
        reply_markup=admin_system_card_keyboard(
            system.id
        ),
    )

@router.callback_query(
    lambda callback: callback.data.startswith(
        "admin:system:deactivate:"
    )
)
async def deactivate_admin_system(
    callback: CallbackQuery,
    state: FSMContext,
    session,
) -> None:
    if not await ensure_admin(callback):
        return

    system_id = int(
        callback.data.split(":")[-1]
    )

    system = await get_system(
        session,
        system_id,
    )

    if system is None or not system.is_active:
        await callback.answer(
            "Система уже отключена.",
            show_alert=True,
        )
        return

    await deactivate_system(
        session,
        system,
    )

    await state.clear()

    systems = await get_systems(
        session,
        "diagnosis",
    )

    text = [
        "⛔ <b>Система отключена</b>",
        "",
        f"<s>{system.name}</s>",
        "",
        "Активные системы:",
        "",
    ]

    if systems:
        for index, item in enumerate(
            systems,
            start=1,
        ):
            text.append(
                f"{index}. {item.name}"
            )
    else:
        text.append(
            "Активных систем нет."
        )

    await callback.message.edit_text(
        "\n".join(text),
        reply_markup=admin_systems_keyboard(
            systems
        ),
    )

    await callback.answer()

@router.callback_query(
    lambda callback: callback.data.startswith(
        "admin:system:problems:"
    )
)
async def admin_system_problems(
    callback: CallbackQuery,
) -> None:
    if not await ensure_admin(callback):
        return

    await callback.answer(
        "Раздел проблем будет добавлен следующим шагом.",
        show_alert=True,
    )


@router.callback_query(
    lambda callback: callback.data.startswith(
        "admin:system:delete_confirm:"
    )
)
async def delete_admin_system_confirm(
    callback: CallbackQuery,
    state: FSMContext,
    session,
) -> None:
    if not await ensure_admin(callback):
        return

    system_id = int(
        callback.data.split(":")[-1]
    )

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

    if system.is_active:
        await callback.answer(
            "Нельзя удалить активную систему.",
            show_alert=True,
        )
        return

    system_name = system.name

    await delete_system(
        session,
        system,
    )

    await state.clear()

    systems = await get_inactive_systems(
        session,
        "diagnosis",
    )

    text = [
        "✅ <b>Система удалена окончательно</b>",
        "",
        f"<s>{system_name}</s>",
        "",
    ]

    if systems:
        text.append("🗑 <b>Отключённые системы:</b>")
        text.append("")

        for index, item in enumerate(
            systems,
            start=1,
        ):
            text.append(
                f"{index}. {item.name}"
            )
    else:
        text.append(
            "Отключённых систем больше нет."
        )

    await callback.message.edit_text(
        "\n".join(text),
        reply_markup=admin_inactive_systems_keyboard(
            systems
        ),
    )

    await callback.answer(
        "Система удалена."
    )