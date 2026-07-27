"""
User Repository
---------------
Layer akses database untuk model User.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Mengambil user berdasarkan Telegram ID."""

        return (
            self.db.query(User)
            .filter(User.telegram_id == telegram_id)
            .first()
        )

    def create(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
        language_code: str | None,
        is_bot: bool,
    ) -> User:
        """Membuat user baru."""

        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            language_code=language_code,
            is_bot=is_bot,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def update(self, user: User, **kwargs) -> User:
        """Memperbarui data user."""

        for key, value in kwargs.items():
            setattr(user, key, value)

        user.last_seen = datetime.utcnow()

        self.db.commit()
        self.db.refresh(user)

        return user