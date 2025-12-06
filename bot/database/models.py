from datetime import datetime
from sqlalchemy import BigInteger, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.core import Base


class Skip(Base):
    __tablename__ = "skips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(50), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    pair_number: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(50), nullable=False)
