from datetime import datetime
from typing import Sequence
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
