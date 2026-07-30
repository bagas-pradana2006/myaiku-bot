"""
Deadline Service
----------------
Business logic untuk pengelolaan Deadline.
"""

from datetime import datetime

from database.session import SessionLocal
from repositories.deadline_repository import DeadlineRepository


class DeadlineService:
    """Service untuk operasi Deadline."""

    def create_deadline(
        self,
        user_id: int,
        title: str,
        deadline_at: datetime,
        description: str | None = None,
        priority: str = "medium",
    ):
        """Membuat deadline baru."""

        db = SessionLocal()

        try:
            repo = DeadlineRepository(db)

            return repo.create(
                user_id=user_id,
                title=title,
                description=description,
                priority=priority,
                deadline_at=deadline_at,
            )

        finally:
            db.close()

    def get_deadlines(
        self,
        user_id: int,
    ):
        """Mengambil seluruh deadline milik user."""

        db = SessionLocal()

        try:
            repo = DeadlineRepository(db)

            return repo.get_all_by_user(user_id)

        finally:
            db.close()

    def get_deadline(
        self,
        user_id: int,
        deadline_id: int,
    ):
        """Mengambil satu deadline berdasarkan ID milik user."""

        db = SessionLocal()

        try:
            repo = DeadlineRepository(db)

            return repo.get_by_id_and_user(
                deadline_id=deadline_id,
                user_id=user_id,
            )

        finally:
            db.close()

    def edit_deadline(
        self,
        user_id: int,
        deadline_id: int,
        title: str,
        deadline_at: datetime,
        description: str | None = None,
        priority: str = "medium",
    ):
        """Mengubah data deadline."""

        db = SessionLocal()

        try:
            repo = DeadlineRepository(db)

            deadline = repo.get_by_id_and_user(
                deadline_id=deadline_id,
                user_id=user_id,
            )

            if not deadline:
                return None

            deadline.title = title
            deadline.description = description
            deadline.priority = priority
            deadline.deadline_at = deadline_at

            return repo.update(deadline)

        finally:
            db.close()

    def complete_deadline(
        self,
        user_id: int,
        deadline_id: int,
    ):
        """Menandai deadline sebagai selesai."""

        db = SessionLocal()

        try:
            repo = DeadlineRepository(db)

            deadline = repo.get_by_id_and_user(
                deadline_id=deadline_id,
                user_id=user_id,
            )

            if not deadline:
                return None

            deadline.is_completed = True
            deadline.completed_at = datetime.utcnow()

            return repo.update(deadline)

        finally:
            db.close()

    def uncomplete_deadline(
        self,
        user_id: int,
        deadline_id: int,
    ):
        """Mengembalikan deadline menjadi belum selesai."""

        db = SessionLocal()

        try:
            repo = DeadlineRepository(db)

            deadline = repo.get_by_id_and_user(
                deadline_id=deadline_id,
                user_id=user_id,
            )

            if not deadline:
                return None

            deadline.is_completed = False
            deadline.completed_at = None

            return repo.update(deadline)

        finally:
            db.close()

    def delete_deadline(
        self,
        user_id: int,
        deadline_id: int,
    ):
        """Menghapus deadline."""

        db = SessionLocal()

        try:
            repo = DeadlineRepository(db)

            deadline = repo.get_by_id_and_user(
                deadline_id=deadline_id,
                user_id=user_id,
            )

            if not deadline:
                return False

            repo.delete(deadline)

            return True

        finally:
            db.close()

    def get_pending_deadlines(self):
        """Mengambil seluruh deadline yang belum selesai."""

        db = SessionLocal()

        try:
            repo = DeadlineRepository(db)

            return repo.get_pending()

        finally:
            db.close()

    def mark_as_notified(
        self,
        deadline_id: int,
    ):
        """
        Menandai deadline sebagai sudah dikirim notifikasi.
        """

        db = SessionLocal()

        try:
            repo = DeadlineRepository(db)

            deadline = repo.get_by_id(
                deadline_id,
            )

            if not deadline:
                return None

            deadline.is_notified = True

            return repo.update(deadline)

        finally:
            db.close()