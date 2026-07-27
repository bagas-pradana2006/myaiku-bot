"""
Todo Callback Handler
---------------------
Menangani seluruh callback Todo.
"""

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from services.todo_service import TodoService
from services.user_service import UserService
from utils.logger import logger
from utils.todo_formatter import build_todo_list

todo_service = TodoService()
user_service = UserService()


async def refresh_todo_list(query, user_id: int):
    """Refresh tampilan todo list."""

    todos = todo_service.get_todos(user_id)

    if not todos:
        await query.edit_message_text(
            "📝 Kamu belum memiliki Todo."
        )
        return

    text, keyboard = build_todo_list(todos)

    await query.edit_message_text(
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


async def todo_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query
    await query.answer()

    data = query.data

    logger.info(
        "Todo callback received: %s",
        data,
    )

    telegram_user = update.effective_user

    db_user = user_service.get_user_by_telegram_id(
        telegram_user.id,
    )

    if not db_user:
        await query.answer(
            "User tidak ditemukan.",
            show_alert=True,
        )
        return

    # ==========================================
    # COMPLETE
    # ==========================================

    if data.startswith("done_"):

        todo_id = int(data.split("_")[1])

        todo = todo_service.complete_todo(
            db_user.id,
            todo_id,
        )

        if not todo:
            await query.answer(
                "Todo tidak ditemukan.",
                show_alert=True,
            )
            return

        await refresh_todo_list(
            query,
            db_user.id,
        )

        return

    # ==========================================
    # UNDO
    # ==========================================

    if data.startswith("undo_"):

        todo_id = int(data.split("_")[1])

        todo = todo_service.uncomplete_todo(
            db_user.id,
            todo_id,
        )

        if not todo:
            await query.answer(
                "Todo tidak ditemukan.",
                show_alert=True,
            )
            return

        await refresh_todo_list(
            query,
            db_user.id,
        )

        return

    # ==========================================
    # DELETE CONFIRM
    # ==========================================

    if data.startswith("delete_confirm_"):

        todo_id = int(data.split("_")[2])

        todo_service.delete_todo(
            db_user.id,
            todo_id,
        )

        await refresh_todo_list(
            query,
            db_user.id,
        )

        return

    # ==========================================
    # DELETE CANCEL
    # ==========================================

    if data == "delete_cancel":

        await refresh_todo_list(
            query,
            db_user.id,
        )

        return

    # ==========================================
    # DELETE
    # ==========================================

    if data.startswith("delete_"):

        todo_id = int(data.split("_")[1])

        todo = todo_service.get_todo(
            db_user.id,
            todo_id,
        )

        if not todo:
            await query.answer(
                "Todo tidak ditemukan.",
                show_alert=True,
            )
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Ya, Hapus",
                        callback_data=f"delete_confirm_{todo.id}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❌ Batal",
                        callback_data="delete_cancel",
                    )
                ],
            ]
        )

        await query.edit_message_text(
            text=(
                "⚠️ <b>Konfirmasi Hapus</b>\n\n"
                f"📝 {todo.title}\n\n"
                "Yakin ingin menghapus todo ini?"
            ),
            parse_mode="HTML",
            reply_markup=keyboard,
        )

        return

    # ==========================================
    # EDIT
    # ==========================================

    if data.startswith("edit_"):

        await query.answer(
            "✏️ Edit Todo (Coming Soon)",
            show_alert=False,
        )

        return

    # ==========================================
    # UNKNOWN
    # ==========================================

    await query.answer(
        "Callback tidak dikenali.",
        show_alert=True,
    )