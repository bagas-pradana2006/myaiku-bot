"""
Todo Helper
-----------
Helper untuk mengambil dan membangun Todo List.
"""

from services.todo_service import TodoService
from services.user_service import UserService
from utils.todo_formatter import build_todo_list

todo_service = TodoService()
user_service = UserService()


def build_user_todo_list(telegram_user):
    """
    Mengambil seluruh Todo user beserta tampilan.
    """

    db_user = user_service.get_user_by_telegram_id(
        telegram_user.id,
    )

    if not db_user:
        return None, None

    todos = todo_service.get_todos(db_user.id)

    text, keyboard = build_todo_list(todos)

    return db_user, (text, keyboard)