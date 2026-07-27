"""
Reminder Handler
----------------
Conversation Handler untuk fitur Reminder.
"""

from datetime import datetime

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from keyboards.main_menu import get_main_menu
from services.reminder_service import ReminderService
from services.user_service import UserService
from utils.logger import logger
from utils.time import wib_to_utc

ASK_TITLE = 1
ASK_DATE = 2
ASK_TIME = 3

reminder_service = ReminderService()
user_service = UserService()


async def reminder_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Memulai proses pembuatan Reminder.
    """

    context.user_data.clear()

    logger.info(
        "Reminder creation started by %s",
        update.effective_user.id,
    )

    await update.message.reply_text(
        "⏰ Apa yang ingin diingatkan?\n\n"
        "Contoh:\n"
        "Bayar UKT",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ASK_TITLE


async def reminder_title(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Menyimpan judul reminder.
    """

    context.user_data["reminder_title"] = (
        update.message.text.strip()
    )

    await update.message.reply_text(
        "📅 Masukkan tanggal.\n\n"
        "Format:\n"
        "27-07-2026",
    )

    return ASK_DATE


async def reminder_date(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Menyimpan tanggal reminder.
    """

    context.user_data["reminder_date"] = (
        update.message.text.strip()
    )

    await update.message.reply_text(
        "🕒 Masukkan jam.\n\n"
        "Format:\n"
        "13:30",
    )

    return ASK_TIME


async def reminder_time(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Menyimpan reminder ke database.
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

    title = context.user_data["reminder_title"]
    date = context.user_data["reminder_date"]
    time = update.message.text.strip()

    try:
        remind_at = wib_to_utc(
            datetime.strptime(
                f"{date} {time}",
                "%d-%m-%Y %H:%M",
            )
        )

    except ValueError:

        await update.message.reply_text(
            "❌ Format tanggal atau jam tidak valid.\n\n"
            "Tanggal : 27-07-2026\n"
            "Jam : 13:30",
        )

        return ASK_TIME

    reminder = reminder_service.create_reminder(
        user_id=db_user.id,
        title=title,
        remind_at=remind_at,
    )

    logger.info(
        "Reminder created | User=%s | Reminder=%s",
        db_user.telegram_id,
        reminder.title,
    )

    context.user_data.clear()

    await update.message.reply_text(
        (
            "✅ Reminder berhasil dibuat.\n\n"
            f"⏰ {reminder.title}\n"
            f"📅 {date} {time}"
        ),
        reply_markup=get_main_menu(),
    )

    return ConversationHandler.END


async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Membatalkan pembuatan Reminder.
    """

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Pembuatan Reminder dibatalkan.",
        reply_markup=get_main_menu(),
    )

    return ConversationHandler.END


reminder_conversation = ConversationHandler(
    entry_points=[
        CommandHandler(
            "reminder",
            reminder_start,
        ),
        MessageHandler(
            filters.Regex("^⏰ Reminder$"),
            reminder_start,
        ),
    ],
    states={
        ASK_TITLE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                reminder_title,
            )
        ],
        ASK_DATE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                reminder_date,
            )
        ],
        ASK_TIME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                reminder_time,
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