from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.database.queries import get_skips
from bot.keyboards import Keyboard
from bot.utils import format_skips
from bot.database.core import session_factory

router = Router()


@router.callback_query(F.data == "my_skips")
async def start_adding_skip_handler(call: CallbackQuery, state: FSMContext):
    async with session_factory() as session:
        skips = await get_skips(session, call.from_user.id)

    if len(skips) == 0:
        await call.answer("📃 У тебя пока нет пропусков")
        return

    skips_text = format_skips(skips)

    await call.message.edit_text(
        f"📃 Мои пропуски\n\n{skips_text}",
        reply_markup=Keyboard.get_back_to_menu_kb(),
    )


@router.callback_query(F.data == "to_main_menu")
async def to_main_menu_handler(call: CallbackQuery):
    await call.message.edit_text(
        "🏠 Главное меню",
        reply_markup=Keyboard.get_main_menu_kb(),
    )
