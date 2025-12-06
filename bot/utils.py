from collections import defaultdict
import datetime
from aiogram.fsm.context import FSMContext

from bot.database.models import Skip
from bot.enums import WhenPair
from bot.schemas import AddingSkipStateSchema

MONTH_NAMES = {
    1: "январь",
    2: "февраль",
    3: "март",
    4: "апрель",
    5: "май",
    6: "июнь",
    7: "июль",
    8: "август",
    9: "сентябрь",
    10: "октябрь",
    11: "ноябрь",
    12: "декабрь",
}


class StatesSerializer:
    @staticmethod
    async def get_adding_skip_schema(state: FSMContext):
        data = await state.get_data()

        return AddingSkipStateSchema(
            when_pair=data["when_pair"],
            pair_number=data["pair_number"],
            subject_name=data["subject_name"],
            reason=data["reason"],
        )


MONTH_NAMES = {
    1: "январь",
    2: "февраль",
    3: "март",
    4: "апрель",
    5: "май",
    6: "июнь",
    7: "июль",
    8: "август",
    9: "сентябрь",
    10: "октябрь",
    11: "ноябрь",
    12: "декабрь",
}


def format_skips(skips: list[Skip]) -> str:
    grouped = defaultdict(lambda: defaultdict(list))

    for skip in skips:
        grouped[skip.date.year][skip.date.month].append(skip)

    result = ""

    for year in sorted(grouped.keys()):
        result += f"<b>{year} год</b>\n"

        for month in sorted(grouped[year].keys()):
            month_name = MONTH_NAMES[month]
            result += f"  └ <b><i>{month_name}</i></b>\n"

            # сортировка по дате + номеру пары
            for skip in sorted(grouped[year][month], key=lambda s: (s.date, s.pair_number)):
                date_str = skip.date.strftime("%d.%m")
                # pair = skip.pair_number

                result += f"      • <b>{date_str}</b> - <i>{skip.subject}</i> — {skip.reason}\n"
        result += "\n"

    return result.strip()


def get_date_by_when_pair(when_pair: WhenPair):
    match when_pair:
        case WhenPair.YESTERDAY:
            return datetime.datetime.now() - datetime.timedelta(days=1)
        case WhenPair.TODAY:
            return datetime.datetime.now()
