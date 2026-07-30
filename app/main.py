"""
Main Entry Point
----------------
Entry point aplikasi MyAiku Bot.
"""

from telegram.request import HTTPXRequest
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config.settings import BOT_TOKEN

from handlers.deadline import deadline_conversation
from handlers.deadline_callback import deadline_callback
from handlers.deadline_list import deadline_list
from handlers.navigation import navigation

from handlers.reminder import reminder_conversation
from handlers.reminder_callback import reminder_callback
from handlers.reminder_list import reminder_list

from handlers.start import help_command, start
from handlers.status import status

from handlers.todo import todo_conversation
from handlers.todo_callback import todo_callback
from handlers.todo_list import todo_list

# --- Import Finance Handler Baru ---
from handlers.finance_list import finance_list
from handlers.finance import finance_conversation
from handlers.finance_callback import finance_callback  
from scheduler.deadline_scheduler import deadline_scheduler
from scheduler.reminder_scheduler import reminder_scheduler

from startup import startup
from utils.error_handler import error_handler
from utils.logger import logger


def build_application() -> Application:
    """
    Membangun instance Telegram Application.
    """

    request = HTTPXRequest(
        connection_pool_size=8,
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30,
    )

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(request)
        .build()
    )

    # ======================================================
    # Command Handlers
    # ======================================================

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))

    app.add_handler(CommandHandler("todos", todo_list))
    app.add_handler(CommandHandler("reminders", reminder_list))
    app.add_handler(CommandHandler("deadlines", deadline_list))
    
    # --- Tambahkan Command Finance ---
    app.add_handler(CommandHandler("finance", finance_list))

    # ======================================================
    # Conversation Handlers
    # ======================================================

    app.add_handler(todo_conversation)
    app.add_handler(reminder_conversation)
    app.add_handler(deadline_conversation)
    
    # --- Tambahkan Conversation Finance ---
    app.add_handler(finance_conversation)

    # ======================================================
    # Callback Query Handlers
    # ======================================================

    app.add_handler(
        CallbackQueryHandler(
            todo_callback,
            pattern=(
                r"^(done_|undo_|edit_|"
                r"delete_|delete_confirm_|delete_cancel$)"
            ),
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            reminder_callback,
            pattern=(
                r"^(reminder_edit_|"
                r"reminder_delete_|"
                r"reminder_delete_confirm_|"
                r"reminder_delete_cancel$)"
            ),
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            deadline_callback,
            pattern=(
                r"^(deadline_done_|"
                r"deadline_undo_|"
                r"deadline_edit_|"
                r"deadline_delete_|"
                r"deadline_delete_confirm_|"
                r"deadline_delete_cancel$)"
            ),
        )
    )

    # --- Tambahkan Callback Finance ---
    app.add_handler(
        CallbackQueryHandler(
            finance_callback,
            pattern=r"^(finance_history|finance_summary|finance_del_.*|finance_delconfirm_.*)$",
        )
    )

    # ======================================================
    # Navigation Handler
    # ======================================================

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            navigation,
        )
    )

    # ======================================================
    # Error Handler
    # ======================================================

    app.add_error_handler(error_handler)

    return app


def main():
    """
    Entry point aplikasi.
    """

    logger.info("Initializing MyAiku Bot...")

    startup()

    application = build_application()

    # ======================================================
    # Scheduler
    # ======================================================

    application.job_queue.run_repeating(
        reminder_scheduler,
        interval=30,
        first=5,
        name="reminder_scheduler",
    )

    application.job_queue.run_repeating(
        deadline_scheduler,
        interval=30,
        first=10,
        name="deadline_scheduler",
    )

    logger.info("Reminder scheduler registered.")
    logger.info("Deadline scheduler registered.")

    logger.info("🚀 MyAiku Bot started successfully.")

    application.run_polling(
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()