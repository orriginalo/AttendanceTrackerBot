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


WEEKDAY_NAMES = {
    0: "понедельник",
    1: "вторник",
    2: "среда",
    3: "четверг",
    4: "пятница",
    5: "суббота",
    6: "воскресенье",
}


def format_stats(skips: list[Skip]) -> str:
    if not skips:
        return "Пока нет данных для статистики. Добавь первый пропуск — и тут появится динамика."

    today = datetime.date.today()
    dates = [s.date for s in skips]

    total = len(skips)
    this_week_start = today - datetime.timedelta(days=today.weekday())
    this_month_start = today.replace(day=1)
    last_30_start = today - datetime.timedelta(days=29)

    this_week = sum(1 for d in dates if d >= this_week_start)
    this_month = sum(1 for d in dates if d >= this_month_start)
    last_30 = sum(1 for d in dates if d >= last_30_start)

    from collections import Counter

    subject_top = Counter(s.subject for s in skips).most_common(1)
    reason_top = Counter(s.reason for s in skips).most_common(1)
    weekday_top = Counter(s.date.weekday() for s in skips).most_common(1)
    pair_top = Counter(s.pair_number for s in skips).most_common(1)

    last_skip = max(skips, key=lambda s: (s.date, s.pair_number))

    unique_dates = sorted(set(dates))
    max_streak = 1
    current_streak = 0
    streak = 1
    for i in range(1, len(unique_dates)):
        if unique_dates[i] == unique_dates[i - 1] + datetime.timedelta(days=1):
            streak += 1
        else:
            max_streak = max(max_streak, streak)
            streak = 1
    max_streak = max(max_streak, streak)

    if today in unique_dates:
        current_streak = 1
        d = today
        while d - datetime.timedelta(days=1) in unique_dates:
            current_streak += 1
            d -= datetime.timedelta(days=1)

    subject_text = f"{subject_top[0][0]} ({subject_top[0][1]})" if subject_top else "—"
    reason_text = f"{reason_top[0][0]} ({reason_top[0][1]})" if reason_top else "—"
    weekday_text = f"{WEEKDAY_NAMES[weekday_top[0][0]]} ({weekday_top[0][1]})" if weekday_top else "—"
    pair_text = f"{pair_top[0][0]} ({pair_top[0][1]})" if pair_top else "—"

    last_date = last_skip.date.strftime("%d.%m.%Y")
    last_line = f"{last_date} • {last_skip.subject} • пара {last_skip.pair_number} • {last_skip.reason}"

    lines = [
        "📊 <b>Статистика пропусков</b>",
        "",
        f"Всего: <b>{total}</b>",
        f"За 7 дней: <b>{this_week}</b>",
        f"За 30 дней: <b>{last_30}</b>",
        f"В этом месяце: <b>{this_month}</b>",
        "",
        "🔥 <b>Топы</b>",
        f"Предмет: <b>{subject_text}</b>",
        f"Причина: <b>{reason_text}</b>",
        f"День недели: <b>{weekday_text}</b>",
        f"Пара: <b>{pair_text}</b>",
        "",
        "📈 <b>Серии</b>",
        f"Текущая серия: <b>{current_streak}</b> дн.",
        f"Лучшая серия: <b>{max_streak}</b> дн.",
        "",
        "🕒 <b>Последний пропуск</b>",
        last_line,
    ]

    return "\n".join(lines)
