"""
User Service
------------
Business logic untuk pengelolaan data pengguna Telegram.
"""

from database.session import SessionLocal
from repositories.user_repository import UserRepository


class UserService:
    """Service untuk operasi User."""

    def save_user(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
        language_code: str | None,
        is_bot: bool,
    ):
        """
        Membuat user baru atau memperbarui data user jika sudah ada.
        """

        db = SessionLocal()

        try:
            repo = UserRepository(db)

            user = repo.get_by_telegram_id(telegram_id)

            if user:
                return repo.update(
                    user,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    language_code=language_code,
                    is_bot=is_bot,
                )

            return repo.create(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                language_code=language_code,
                is_bot=is_bot,
            )

        finally:
            db.close()

    def get_user_by_telegram_id(
        self,
        telegram_id: int,
    ):
        """
        Mengambil user berdasarkan Telegram ID.
        """

        db = SessionLocal()

        try:
            repo = UserRepository(db)

            return repo.get_by_telegram_id(telegram_id)

        finally:
            db.close()