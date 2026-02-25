from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.core import session_factory
from bot.database.queries import get_skips
from bot.keyboards import Keyboard
from bot.utils import format_stats

router = Router()


@router.callback_query(F.data == "show_stats")
async def start_adding_skip_handler(call: CallbackQuery):
    async with session_factory() as session:
        skips = await get_skips(session, call.from_user.id)

    stats_text = format_stats(skips)

    await call.message.edit_text(
        stats_text,
        reply_markup=Keyboard.get_stats_kb(),
    )
