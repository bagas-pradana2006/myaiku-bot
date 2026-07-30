"""
Finance Model
-------------
Menyimpan data pemasukan (income) dan pengeluaran (expense) pengguna.
"""

import enum
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    BigInteger,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Finance(Base):
    __tablename__ = "finances"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType),
        nullable=False,
    )

    amount: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationship
    user = relationship("User")