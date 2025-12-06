from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "show_stats")
async def start_adding_skip_handler(call: CallbackQuery):
    await call.answer("⛔ Эта функция пока не доступна", show_alert=True)
