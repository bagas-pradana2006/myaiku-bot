"""
Reminder Repository
-------------------
Layer akses database untuk model Reminder.
"""

from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from models.reminder import Reminder
from utils.time import now_utc


class ReminderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        title: str,
        remind_at: datetime,
    ) -> Reminder:
        """Membuat reminder baru."""

        reminder = Reminder(
            user_id=user_id,
            title=title,
            remind_at=remind_at,
        )

        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)

        return reminder

    def get_all_by_user(
        self,
        user_id: int,
    ) -> list[Reminder]:
        """Mengambil seluruh reminder milik user."""

        return (
            self.db.query(Reminder)
            .filter(Reminder.user_id == user_id)
            .order_by(Reminder.remind_at.asc())
            .all()
        )

    def get_by_id(
        self,
        reminder_id: int,
    ) -> Reminder | None:
        """Mengambil reminder berdasarkan ID."""

        return (
            self.db.query(Reminder)
            .filter(Reminder.id == reminder_id)
            .first()
        )

    def get_by_id_and_user(
        self,
        reminder_id: int,
        user_id: int,
    ) -> Reminder | None:
        """
        Mengambil reminder berdasarkan ID
        dan memastikan reminder tersebut milik user.
        """

        return (
            self.db.query(Reminder)
            .filter(
                Reminder.id == reminder_id,
                Reminder.user_id == user_id,
            )
            .first()
        )

    def get_pending(self) -> list[Reminder]:
        """Mengambil reminder yang siap dikirim."""

        return (
            self.db.query(Reminder)
            .options(
                joinedload(Reminder.user),
            )
            .filter(
                Reminder.is_sent.is_(False),
                Reminder.remind_at <= now_utc(),
            )
            .order_by(Reminder.remind_at.asc())
            .all()
        )

    def update(
        self,
        reminder: Reminder,
    ) -> Reminder:
        """Menyimpan perubahan reminder."""

        self.db.commit()
        self.db.refresh(reminder)

        return reminder

    def delete(
        self,
        reminder: Reminder,
    ) -> None:
        """Menghapus reminder."""

        self.db.delete(reminder)
        self.db.commit()