"""
Edit Todo Handler
-----------------
Conversation Handler untuk mengubah judul Todo.
"""

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from keyboards.main_menu import get_main_menu
from services.todo_service import TodoService
from services.user_service import UserService
from utils.logger import logger

ASK_NEW_TITLE = 1

todo_service = TodoService()
user_service = UserService()


async def edit_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Memulai proses edit Todo.
    """

    todo_id = context.user_data.get("edit_todo_id")

    if not todo_id:
        await update.message.reply_text(
            "❌ Todo tidak ditemukan.",
            reply_markup=get_main_menu(),
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "✏️ Masukkan judul baru:",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ASK_NEW_TITLE


async def edit_title(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Menyimpan perubahan Todo.
    """

    telegram_user = update.effective_user

    db_user = user_service.get_user_by_telegram_id(
        telegram_user.id,
    )

    if not db_user:
        await update.message.reply_text(
            "❌ User tidak ditemukan.",
            reply_markup=get_main_menu(),
        )
        return ConversationHandler.END

    todo_id = context.user_data.get("edit_todo_id")

    if not todo_id:
        await update.message.reply_text(
            "❌ Todo tidak ditemukan.",
            reply_markup=get_main_menu(),
        )
        return ConversationHandler.END

    new_title = update.message.text.strip()

    todo = todo_service.edit_todo(
        user_id=db_user.id,
        todo_id=todo_id,
        title=new_title,
    )

    if not todo:
        await update.message.reply_text(
            "❌ Todo tidak ditemukan.",
            reply_markup=get_main_menu(),
        )
        return ConversationHandler.END

    logger.info(
        "Todo edited | User=%s | Todo=%s",
        db_user.telegram_id,
        todo.title,
    )

    context.user_data.pop(
        "edit_todo_id",
        None,
    )

    await update.message.reply_text(
        (
            "✅ Todo berhasil diperbarui.\n\n"
            f"📝 {todo.title}"
        ),
        reply_markup=get_main_menu(),
    )

    return ConversationHandler.END


async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Membatalkan edit Todo.
    """

    context.user_data.pop(
        "edit_todo_id",
        None,
    )

    await update.message.reply_text(
        "❌ Edit Todo dibatalkan.",
        reply_markup=get_main_menu(),
    )

    return ConversationHandler.END


edit_todo_conversation = ConversationHandler(
    entry_points=[
        CommandHandler(
            "edit_todo",
            edit_start,
        ),
    ],
    states={
        ASK_NEW_TITLE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                edit_title,
            )
        ],
    },
    fallbacks=[
        CommandHandler(
            "cancel",
            cancel,
        )
    ],
)