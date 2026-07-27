"""
Todo Service
------------
Business logic untuk pengelolaan Todo.
"""

from datetime import datetime

from database.session import SessionLocal
from repositories.todo_repository import TodoRepository


class TodoService:
    """Service untuk operasi Todo."""

    def create_todo(
        self,
        user_id: int,
        title: str,
        description: str | None = None,
    ):
        """Membuat todo baru."""

        db = SessionLocal()

        try:
            repo = TodoRepository(db)

            return repo.create(
                user_id=user_id,
                title=title,
                description=description,
            )

        finally:
            db.close()

    def get_todos(
        self,
        user_id: int,
    ):
        """Mengambil seluruh todo milik user."""

        db = SessionLocal()

        try:
            repo = TodoRepository(db)

            return repo.get_all_by_user(user_id)

        finally:
            db.close()

    def get_todo(
        self,
        user_id: int,
        todo_id: int,
    ):
        """Mengambil satu todo berdasarkan ID milik user."""

        db = SessionLocal()

        try:
            repo = TodoRepository(db)

            return repo.get_by_id_and_user(
                todo_id=todo_id,
                user_id=user_id,
            )

        finally:
            db.close()

    def edit_todo(
        self,
        user_id: int,
        todo_id: int,
        title: str,
        description: str | None = None,
    ):
        """Mengubah data todo."""

        db = SessionLocal()

        try:
            repo = TodoRepository(db)

            todo = repo.get_by_id_and_user(
                todo_id=todo_id,
                user_id=user_id,
            )

            if not todo:
                return None

            todo.title = title
            todo.description = description

            return repo.update(todo)

        finally:
            db.close()

    def complete_todo(
        self,
        user_id: int,
        todo_id: int,
    ):
        """Menandai todo sebagai selesai."""

        db = SessionLocal()

        try:
            repo = TodoRepository(db)

            todo = repo.get_by_id_and_user(
                todo_id=todo_id,
                user_id=user_id,
            )

            if not todo:
                return None

            todo.is_completed = True
            todo.completed_at = datetime.utcnow()

            return repo.update(todo)

        finally:
            db.close()

    def uncomplete_todo(
        self,
        user_id: int,
        todo_id: int,
    ):
        """Mengembalikan todo menjadi belum selesai."""

        db = SessionLocal()

        try:
            repo = TodoRepository(db)

            todo = repo.get_by_id_and_user(
                todo_id=todo_id,
                user_id=user_id,
            )

            if not todo:
                return None

            todo.is_completed = False
            todo.completed_at = None

            return repo.update(todo)

        finally:
            db.close()

    def delete_todo(
        self,
        user_id: int,
        todo_id: int,
    ):
        """Menghapus todo."""

        db = SessionLocal()

        try:
            repo = TodoRepository(db)

            todo = repo.get_by_id_and_user(
                todo_id=todo_id,
                user_id=user_id,
            )

            if not todo:
                return False

            repo.delete(todo)

            return True

        finally:
            db.close()