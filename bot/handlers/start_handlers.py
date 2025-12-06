from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .utils import send_main_menu

router = Router()


@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.clear()
    await send_main_menu(msg.chat.id, msg)
