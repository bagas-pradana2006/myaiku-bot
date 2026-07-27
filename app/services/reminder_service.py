"""
Reminder Service
----------------
Business logic untuk pengelolaan Reminder.
"""

from datetime import datetime

from database.session import SessionLocal
from repositories.reminder_repository import ReminderRepository


class ReminderService:
    """Service untuk operasi Reminder."""

    def create_reminder(
        self,
        user_id: int,
        title: str,
        remind_at: datetime,
    ):
        """Membuat reminder baru."""

        db = SessionLocal()

        try:
            repo = ReminderRepository(db)

            return repo.create(
                user_id=user_id,
                title=title,
                remind_at=remind_at,
            )

        finally:
            db.close()

    def get_reminders(
        self,
        user_id: int,
    ):
        """Mengambil seluruh reminder milik user."""

        db = SessionLocal()

        try:
            repo = ReminderRepository(db)

            return repo.get_all_by_user(user_id)

        finally:
            db.close()

    def get_reminder(
        self,
        user_id: int,
        reminder_id: int,
    ):
        """Mengambil satu reminder berdasarkan ID milik user."""

        db = SessionLocal()

        try:
            repo = ReminderRepository(db)

            return repo.get_by_id_and_user(
                reminder_id=reminder_id,
                user_id=user_id,
            )

        finally:
            db.close()

    def get_pending_reminders(self):
        """Mengambil seluruh reminder yang belum dikirim."""

        db = SessionLocal()

        try:
            repo = ReminderRepository(db)

            return repo.get_pending()

        finally:
            db.close()

    def mark_as_sent(
        self,
        reminder_id: int,
    ):
        """Menandai reminder sebagai sudah dikirim."""

        db = SessionLocal()

        try:
            repo = ReminderRepository(db)

            reminder = repo.get_by_id(reminder_id)

            if not reminder:
                return None

            reminder.is_sent = True

            return repo.update(reminder)

        finally:
            db.close()

    def delete_reminder(
        self,
        user_id: int,
        reminder_id: int,
    ):
        """Menghapus reminder."""

        db = SessionLocal()

        try:
            repo = ReminderRepository(db)

            reminder = repo.get_by_id_and_user(
                reminder_id=reminder_id,
                user_id=user_id,
            )

            if not reminder:
                return False

            repo.delete(reminder)

            return True

        finally:
            db.close()