"""
Todo Handler
------------
Conversation Handler untuk fitur Todo.
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

ASK_TITLE = 1

todo_service = TodoService()
user_service = UserService()


async def todo_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Memulai proses pembuatan Todo.
    """

    # Pastikan tidak sedang mode edit
    context.user_data.pop("edit_todo_id", None)

    logger.info(
        "Todo creation started by %s",
        update.effective_user.id,
    )

    await update.message.reply_text(
        "📝 Apa yang ingin kamu kerjakan?\n\n"
        "Contoh:\n"
        "Belajar Docker",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ASK_TITLE


async def todo_title(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Menyimpan Todo ke database.
    """

    telegram_user = update.effective_user

    db_user = user_service.save_user(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name,
        language_code=telegram_user.language_code,
        is_bot=telegram_user.is_bot,
    )

    todo = todo_service.create_todo(
        user_id=db_user.id,
        title=update.message.text.strip(),
    )

    logger.info(
        "Todo created | User=%s | Todo=%s",
        db_user.telegram_id,
        todo.title,
    )

    await update.message.reply_text(
        (
            "✅ Todo berhasil dibuat.\n\n"
            f"📝 {todo.title}\n\n"
            "Kembali ke Main Menu."
        ),
        reply_markup=get_main_menu(),
    )

    return ConversationHandler.END


async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Membatalkan pembuatan Todo.
    """

    context.user_data.pop("edit_todo_id", None)

    await update.message.reply_text(
        "❌ Pembuatan Todo dibatalkan.",
        reply_markup=get_main_menu(),
    )

    return ConversationHandler.END


todo_conversation = ConversationHandler(
    entry_points=[
        CommandHandler(
            "todo",
            todo_start,
        ),
        MessageHandler(
            filters.Regex("^📝 Todo$"),
            todo_start,
        ),
    ],
    states={
        ASK_TITLE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                todo_title,
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