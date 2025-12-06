from aiogram.types import CallbackQuery, Message
from bot.keyboards import Keyboard


async def send_main_menu(chat_id: int, msg_or_call: Message | CallbackQuery):
    await msg_or_call.bot.send_message(chat_id, "🏠 Главное меню", reply_markup=Keyboard.get_main_menu_kb())
