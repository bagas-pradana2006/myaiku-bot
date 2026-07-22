from sqlalchemy.orm import Session

from models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
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
    ) -> User:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user