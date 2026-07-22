from database.session import SessionLocal
from repositories.user_repository import UserRepository


class UserService:
    def save_user(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str,
    ):
        db = SessionLocal()

        try:
            repo = UserRepository(db)

            user = repo.get_by_telegram_id(telegram_id)

            if user:
                return user

            return repo.create(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
            )
        finally:
            db.close()