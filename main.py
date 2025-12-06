import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.database.core import create_tables
from bot.handlers.add_skip_handlers import router as add_skip_router
from bot.handlers.my_skips_handlers import router as my_skips_router
from bot.handlers.start_handlers import router as start_router
from bot.handlers.show_statistics_handlers import router as show_stats_router
from config import settings


bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def main():
    await create_tables()
    print("DB Tables created.")
    dp.include_routers(start_router, add_skip_router, my_skips_router, show_stats_router)
    print("Bot started.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping...")
