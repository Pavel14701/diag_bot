from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.keyboards.main import main_menu_keyboard
from app.services.admin import is_admin


router = Router()


@router.callback_query(
    lambda callback: callback.data == "menu:main"
)
async def back_to_main_menu(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.clear()

    user_id = callback.from_user.id

    await callback.message.edit_text(
        "📋 <b>Главное меню</b>\n\n"
        "Выберите нужный раздел:",
        reply_markup=main_menu_keyboard(
            is_admin(user_id)
        ),
    )

    await callback.answer()