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
    # Группировка данных (оставляем вашу логику)
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for skip in skips:
        month = skip.date.month
        semester = 1 if (9 <= month <= 12) else 2
        grouped[semester][skip.date.year][month].append(skip)

    if not skips:
        return "🤷‍♂️ Пропусков не найдено."

    sections = []

    for semester in sorted(grouped.keys()):
        # Заголовок семестра с разделителем
        sem_header = f"<b>{semester} СЕМЕСТР</b>"
        semester_text = [f"🎓 {sem_header}", "—" * 22]

        for year in sorted(grouped[semester].keys()):
            for month in sorted(grouped[semester][year].keys()):
                month_name = MONTH_NAMES[month].capitalize()
                semester_text.append(f"\n🗓 <b>{month_name} {year}</b>")

                # Сортировка по дате и номеру пары
                sorted_skips = sorted(grouped[semester][year][month], key=lambda s: (s.date, s.pair_number))

                for skip in sorted_skips:
                    date_str = skip.date.strftime("%d.%m")
                    # Добавляем номер пары. Используем [ ] или просто цифру с символом
                    # Например: [2] или 2️⃣
                    pair_info = f"[{skip.pair_number}]"

                    line = f"  ▫️ {pair_info} <code>{date_str}</code> — <b>{skip.subject}</b>\n      └ <i>{skip.reason}</i>"
                    semester_text.append(line)

        sections.append("\n".join(semester_text))

    return "\n\n".join(sections).strip()


def get_date_by_when_pair(when_pair: WhenPair):
    match when_pair:
        case WhenPair.YESTERDAY:
            return datetime.datetime.now() - datetime.timedelta(days=1)
        case WhenPair.TODAY:
            return datetime.datetime.now()
