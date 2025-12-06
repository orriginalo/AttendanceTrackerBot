from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.queries import get_skips
from bot.keyboards import Keyboard
from bot.utils import format_skips
from .utils import send_main_menu
from bot.database.core import session_factory

router = Router()


@router.callback_query(F.data == "show_stats")
async def start_adding_skip_handler(call: CallbackQuery):
    await call.answer("⛔ Эта функция пока не доступна", show_alert=True)
