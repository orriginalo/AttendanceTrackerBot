from datetime import datetime
from typing import Sequence
from collections import Counter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Skip


async def get_skips(session: AsyncSession, tg_id: int) -> Sequence[Skip]:
    stmt = select(Skip).where(Skip.user_tg_id == tg_id)
    result = await session.execute(stmt)
    skips = result.scalars().all()

    return skips


async def add_skip(session: AsyncSession, user_tg_id: int, date: datetime, pair_number: int, subject_name: str, reason: str):
    skip = Skip(
        user_tg_id=user_tg_id,
        date=date,
        pair_number=pair_number,
        subject=subject_name,
        reason=reason,
    )

    session.add(skip)

    return skip


async def get_subjects(session: AsyncSession, tg_id: int, limit: int = 6) -> list[str]:
    stmt = select(Skip.subject).where(Skip.user_tg_id == tg_id)
    result = await session.execute(stmt)
    subjects = result.scalars().all()

    if not subjects:
        return []

    counts = Counter(subjects)
    top = sorted(counts.items(), key=lambda x: (-x[1], x[0].lower()))

    return [name for name, _ in top[:limit]]
