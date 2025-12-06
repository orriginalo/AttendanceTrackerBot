from aiogram.types import InlineKeyboardMarkup as IKMR, InlineKeyboardButton as IKB
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.enums import WhenPair

from config import settings


class PairNumberCBD(CallbackData, prefix="pair_number"):
    number: int


class WhenPairCBD(CallbackData, prefix="when_pair"):
    when_pair: WhenPair


class ReasonCBD(CallbackData, prefix="reason"):
    reason_idx: int


class Keyboard:
    @staticmethod
    def get_back_to_menu_kb():
        return IKMR(
            inline_keyboard=[
                [
                    IKB(text="« Главное меню", callback_data="to_main_menu"),
                ],
            ]
        )

    @staticmethod
    def get_empty_inline_kb():
        return IKMR(inline_keyboard=[[]])

    @staticmethod
    def get_main_menu_kb():
        return IKMR(
            inline_keyboard=[
                [
                    IKB(text="➕ Добавить пропуск", callback_data="add_skip"),
                    IKB(text="Посмотреть статистику 📊", callback_data="show_stats"),
                ],
                [
                    IKB(text="📃 Мои пропуски", callback_data="my_skips"),
                ],
            ]
        )

    @staticmethod
    def get_pair_numbers_kb():
        kb = InlineKeyboardBuilder()
        for number in range(1, 9):
            kb.row(IKB(text=str(number), callback_data=PairNumberCBD(number=number).pack()))

        return kb.as_markup()

    @staticmethod
    def get_when_pair_kb():
        return IKMR(
            inline_keyboard=[
                [
                    IKB(text="◀️ Вчера", callback_data=WhenPairCBD(when_pair=WhenPair.YESTERDAY).pack()),
                    IKB(text="Сегодня ⬇️", callback_data=WhenPairCBD(when_pair=WhenPair.TODAY).pack()),
                ],
            ]
        )

    @staticmethod
    def get_reason_kb():
        kb = InlineKeyboardBuilder()
        for i, reason in enumerate(settings.REASONS):
            kb.row(IKB(text=reason, callback_data=ReasonCBD(reason_idx=i).pack()))

        return kb.as_markup()
