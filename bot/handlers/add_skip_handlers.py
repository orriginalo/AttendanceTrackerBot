from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.database.queries import add_skip
from bot.enums import WhenPair
from .utils import send_main_menu
from bot.keyboards import Keyboard, PairNumberCBD, ReasonCBD, WhenPairCBD
from bot.utils import StatesSerializer, get_date_by_when_pair
from config import settings
from bot.database.core import session_factory

router = Router()


class AddingSkipSG(StatesGroup):
    WHEN_PAIR = State()
    PAIR_NUMBER = State()
    SUBJECT_NAME = State()
    REASON = State()


@router.callback_query(F.data == "add_skip")
async def start_adding_skip_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(AddingSkipSG.WHEN_PAIR)
    await call.message.delete()
    await call.message.answer(
        "[1/4] 📝 Когда была пара?",
        reply_markup=Keyboard.get_when_pair_kb(),
    )


@router.callback_query(AddingSkipSG.WHEN_PAIR, WhenPairCBD.filter())
async def when_pair_handler(call: CallbackQuery, callback_data: WhenPairCBD, state: FSMContext):
    await call.answer(" ")
    await state.update_data(when_pair=callback_data.when_pair)

    when_pair_text = "Вчера" if callback_data.when_pair == WhenPair.YESTERDAY else "Сегодня"
    await call.message.edit_text(
        text=f"[1/4] 📝 Когда была пара? - <b>{when_pair_text}</b>", reply_markup=Keyboard.get_empty_inline_kb()
    )

    await state.set_state(AddingSkipSG.PAIR_NUMBER)
    await call.message.answer(
        "[2/4] 📝 Какой по счету была пара?",
        reply_markup=Keyboard.get_pair_numbers_kb(),
    )


@router.callback_query(AddingSkipSG.PAIR_NUMBER, PairNumberCBD.filter())
async def pair_number_handler(call: CallbackQuery, callback_data: PairNumberCBD, state: FSMContext):
    await call.answer(" ")
    await state.update_data(pair_number=callback_data.number)

    await call.message.edit_text(
        text=f"[2/4] 📝 Какой по счету была пара? - <b>{callback_data.number}</b>", reply_markup=Keyboard.get_empty_inline_kb()
    )

    await state.set_state(AddingSkipSG.SUBJECT_NAME)
    sent = await call.message.answer(
        "[3/4] ✍️ Какой предмет?",
    )
    await state.update_data(subject_msg_id=sent.message_id)


@router.message(AddingSkipSG.SUBJECT_NAME)
async def subject_name_handler(msg: Message, state: FSMContext):
    await state.update_data(subject_name=msg.text)

    msg_id = (await state.get_data())["subject_msg_id"]

    await msg.bot.edit_message_text(
        text=f"[3/4] ✍️ Какой предмет? - <b>{msg.text}</b>",
        reply_markup=Keyboard.get_empty_inline_kb(),
        chat_id=msg.chat.id,
        message_id=msg_id,
    )
    await msg.delete()

    await state.set_state(AddingSkipSG.REASON)
    sent = await msg.answer(
        "[4/4] 📝 Почему пропустил?\n<i>Выбери из списка ниже или напиши свое</i>",
        reply_markup=Keyboard.get_reason_kb(),
    )
    await state.update_data(reason_msg_id=sent.message_id)


@router.callback_query(AddingSkipSG.REASON, ReasonCBD.filter())
async def reason_handler(call: CallbackQuery, callback_data: ReasonCBD, state: FSMContext):
    await call.answer(" ")
    await state.update_data(reason=settings.REASONS[callback_data.reason_idx])

    await call.message.edit_text(
        text=f"[4/4] 📝 Почему пропустил? - <b>{settings.REASONS[callback_data.reason_idx]}</b>",
        reply_markup=Keyboard.get_empty_inline_kb(),
    )

    data = await StatesSerializer.get_adding_skip_schema(state)
    async with session_factory() as session:
        date = get_date_by_when_pair(data.when_pair)
        await add_skip(session, call.from_user.id, date, data.pair_number, data.subject_name, data.reason)
        await session.commit()

    await state.clear()
    await call.message.answer(
        "✅ Пропуск добавлен!",
    )
    await send_main_menu(call.message.chat.id, call)


@router.message(AddingSkipSG.REASON, F.text)
async def self_reason_handler(msg: Message, state: FSMContext):
    await state.update_data(reason=msg.text)

    msg_id = (await state.get_data())["reason_msg_id"]

    await msg.bot.edit_message_text(
        text=f"[4/4] 📝 Почему пропустил? - <b>{msg.text}</b>",
        reply_markup=Keyboard.get_empty_inline_kb(),
        chat_id=msg.chat.id,
        message_id=msg_id,
    )
    await msg.delete()

    data = await StatesSerializer.get_adding_skip_schema(state)
    async with session_factory() as session:
        date = get_date_by_when_pair(data.when_pair)
        await add_skip(session, msg.from_user.id, date, data.pair_number, data.subject_name, data.reason)
        await session.commit()

    await state.clear()
    await msg.answer(
        "✅ Пропуск добавлен!",
    )
    await send_main_menu(msg.chat.id, msg)
