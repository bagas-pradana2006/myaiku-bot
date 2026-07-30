"""
Deadline Repository
-------------------
Layer akses database untuk model Deadline.
"""

from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from models.deadline import Deadline


class DeadlineRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        title: str,
        deadline_at: datetime,
        description: str | None = None,
        priority: str = "medium",
    ) -> Deadline:
        """Membuat deadline baru."""

        deadline = Deadline(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            deadline_at=deadline_at,
        )

        self.db.add(deadline)
        self.db.commit()
        self.db.refresh(deadline)

        return deadline

    def get_all_by_user(
        self,
        user_id: int,
    ) -> list[Deadline]:
        """Mengambil seluruh deadline milik user."""

        return (
            self.db.query(Deadline)
            .filter(Deadline.user_id == user_id)
            .order_by(Deadline.deadline_at.asc())
            .all()
        )

    def get_by_id(
        self,
        deadline_id: int,
    ) -> Deadline | None:
        """Mengambil deadline berdasarkan ID."""

        return (
            self.db.query(Deadline)
            .filter(Deadline.id == deadline_id)
            .first()
        )

    def get_by_id_and_user(
        self,
        deadline_id: int,
        user_id: int,
    ) -> Deadline | None:
        """
        Mengambil deadline berdasarkan ID
        dan memastikan deadline tersebut milik user.
        """

        return (
            self.db.query(Deadline)
            .filter(
                Deadline.id == deadline_id,
                Deadline.user_id == user_id,
            )
            .first()
        )

    def get_pending(
        self,
    ) -> list[Deadline]:
        """
        Mengambil seluruh deadline yang
        sudah jatuh tempo, belum selesai,
        dan belum pernah dikirim notifikasi.
        """

        return (
            self.db.query(Deadline)
            .options(
                joinedload(Deadline.user),
            )
            .filter(
                Deadline.is_completed.is_(False),
                Deadline.is_notified.is_(False),
                Deadline.deadline_at <= datetime.utcnow(),
            )
            .order_by(Deadline.deadline_at.asc())
            .all()
        )

    def update(
        self,
        deadline: Deadline,
    ) -> Deadline:
        """Menyimpan perubahan deadline."""

        self.db.commit()
        self.db.refresh(deadline)

        return deadline

    def delete(
        self,
        deadline: Deadline,
    ) -> None:
        """Menghapus deadline."""

        self.db.delete(deadline)
        self.db.commit()