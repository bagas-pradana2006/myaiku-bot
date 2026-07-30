"""
Navigation Handler
------------------
Menangani seluruh navigasi menu MyAiku.
"""

from telegram import Update
from telegram.ext import ContextTypes

from handlers.finance_list import finance_list
from handlers.deadline import deadline_start
from handlers.menu import back_to_main_menu
from handlers.productivity import productivity_menu
from handlers.reminder import reminder_start
from handlers.todo import todo_start
from keyboards.main_menu import get_main_menu
from services.todo_service import TodoService
from services.user_service import UserService


todo_service = TodoService()
user_service = UserService()


async def navigation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    text = update.message.text.strip()

    # =====================================================
    # EDIT TODO MODE
    # =====================================================

    if "edit_todo_id" in context.user_data:

        todo_id = context.user_data.pop("edit_todo_id")

        telegram_user = update.effective_user

        db_user = user_service.get_user_by_telegram_id(
            telegram_user.id,
        )

        if not db_user:

            await update.message.reply_text(
                "❌ User tidak ditemukan.",
                reply_markup=get_main_menu(),
            )

            return

        todo = todo_service.edit_todo(
            user_id=db_user.id,
            todo_id=todo_id,
            title=text,
        )

        if not todo:

            await update.message.reply_text(
                "❌ Todo tidak ditemukan.",
                reply_markup=get_main_menu(),
            )

            return

        await update.message.reply_text(
            (
                "✅ Todo berhasil diperbarui.\n\n"
                f"📝 {todo.title}"
            ),
            reply_markup=get_main_menu(),
        )

        return

    # =====================================================
    # MENU
    # =====================================================

    if text == "📋 Productivity":
        return await productivity_menu(update, context)

    if text == "📝 Todo":
        return await todo_start(update, context)

    if text == "⏰ Reminder":
        return await reminder_start(update, context)

    if text == "📅 Deadline":
        return await deadline_start(update, context)
        
    # --- Tambahkan routing ke Finance di sini ---
    if "Finance" in text or "Keuangan" in text:
        return await finance_list(update, context)

    if text == "⬅️ Kembali":
        return await back_to_main_menu(update, context)

    await update.message.reply_text(
        "🚧 Fitur ini belum tersedia."
    )