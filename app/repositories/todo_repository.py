"""
Todo Repository
---------------
Layer akses database untuk model Todo.
"""

from sqlalchemy.orm import Session

from models.todo import Todo


class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        title: str,
        description: str | None = None,
    ) -> Todo:
        """Membuat todo baru."""

        todo = Todo(
            user_id=user_id,
            title=title,
            description=description,
        )

        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)

        return todo

    def get_all_by_user(
        self,
        user_id: int,
    ) -> list[Todo]:
        """Mengambil seluruh todo milik user."""

        return (
            self.db.query(Todo)
            .filter(Todo.user_id == user_id)
            .order_by(Todo.created_at.desc())
            .all()
        )

    def get_by_id(
        self,
        todo_id: int,
    ) -> Todo | None:
        """Mengambil todo berdasarkan ID."""

        return (
            self.db.query(Todo)
            .filter(Todo.id == todo_id)
            .first()
        )

    def get_by_id_and_user(
        self,
        todo_id: int,
        user_id: int,
    ) -> Todo | None:
        """
        Mengambil todo berdasarkan ID
        dan memastikan todo tersebut milik user.
        """

        return (
            self.db.query(Todo)
            .filter(
                Todo.id == todo_id,
                Todo.user_id == user_id,
            )
            .first()
        )

    def update(self, todo: Todo) -> Todo:
        """Menyimpan perubahan todo."""

        self.db.commit()
        self.db.refresh(todo)

        return todo

    def delete(self, todo: Todo) -> None:
        """Menghapus todo."""

        self.db.delete(todo)
        self.db.commit()