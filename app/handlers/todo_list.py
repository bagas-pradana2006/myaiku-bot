"""
Todo List Handler
-----------------
Menampilkan seluruh Todo milik user.
"""

from telegram import Update
from telegram.ext import ContextTypes

from services.todo_service import TodoService
from services.user_service import UserService
from utils.logger import logger
from utils.todo_formatter import build_todo_list

todo_service = TodoService()
user_service = UserService()


async def todo_list(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Menampilkan daftar Todo milik user."""

    telegram_user = update.effective_user

    db_user = user_service.save_user(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name,
        language_code=telegram_user.language_code,
        is_bot=telegram_user.is_bot,
    )

    todos = todo_service.get_todos(db_user.id)

    if not todos:
        await update.message.reply_text(
            "📝 Kamu belum memiliki Todo."
        )
        return

    text, keyboard = build_todo_list(todos)

    logger.info(
        "Todo list requested | User=%s | Total=%s",
        db_user.telegram_id,
        len(todos),
    )

    await update.message.reply_text(
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )