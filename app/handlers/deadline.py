"""
Deadline Handler
----------------
Conversation Handler untuk fitur Deadline.
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
from services.deadline_service import DeadlineService
from services.user_service import UserService
from utils.logger import logger
from utils.time import wib_to_utc

ASK_TITLE = 1
ASK_DESCRIPTION = 2
ASK_DATE = 3
ASK_TIME = 4

deadline_service = DeadlineService()
user_service = UserService()


async def deadline_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Memulai proses pembuatan Deadline.
    """

    context.user_data.clear()

    logger.info(
        "Deadline creation started by %s",
        update.effective_user.id,
    )

    await update.message.reply_text(
        "📅 Apa judul deadline?\n\n"
        "Contoh:\n"
        "Tugas Basis Data",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ASK_TITLE


async def deadline_title(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Menyimpan judul deadline.
    """

    context.user_data["deadline_title"] = (
        update.message.text.strip()
    )

    await update.message.reply_text(
        "📝 Masukkan deskripsi.\n\n"
        "Ketik /skip jika tidak ada.",
    )

    return ASK_DESCRIPTION


async def deadline_description(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Menyimpan deskripsi deadline.
    """

    context.user_data["deadline_description"] = (
        update.message.text.strip()
    )

    await update.message.reply_text(
        "📅 Masukkan tanggal deadline.\n\n"
        "Format:\n"
        "27-07-2026",
    )

    return ASK_DATE


async def skip_description(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Melewati pengisian deskripsi.
    """

    context.user_data["deadline_description"] = None

    await update.message.reply_text(
        "📅 Masukkan tanggal deadline.\n\n"
        "Format:\n"
        "27-07-2026",
    )

    return ASK_DATE


async def deadline_date(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Menyimpan tanggal deadline.
    """

    context.user_data["deadline_date"] = (
        update.message.text.strip()
    )

    await update.message.reply_text(
        "🕒 Masukkan jam deadline.\n\n"
        "Format:\n"
        "13:30",
    )

    return ASK_TIME


async def deadline_time(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Menyimpan deadline ke database.
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

    title = context.user_data["deadline_title"]
    description = context.user_data["deadline_description"]
    date = context.user_data["deadline_date"]
    time = update.message.text.strip()

    try:
        deadline_at = wib_to_utc(
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

    deadline = deadline_service.create_deadline(
        user_id=db_user.id,
        title=title,
        description=description,
        deadline_at=deadline_at,
    )

    logger.info(
        "Deadline created | User=%s | Deadline=%s",
        db_user.telegram_id,
        deadline.title,
    )

    context.user_data.clear()

    await update.message.reply_text(
        (
            "✅ Deadline berhasil dibuat.\n\n"
            f"📅 {deadline.title}\n"
            f"🗓 {date} {time}"
        ),
        reply_markup=get_main_menu(),
    )

    return ConversationHandler.END


async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """
    Membatalkan pembuatan Deadline.
    """

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Pembuatan Deadline dibatalkan.",
        reply_markup=get_main_menu(),
    )

    return ConversationHandler.END


deadline_conversation = ConversationHandler(
    entry_points=[
        CommandHandler(
            "deadline",
            deadline_start,
        ),
        MessageHandler(
            filters.Regex("^📅 Deadline$"),
            deadline_start,
        ),
    ],
    states={
        ASK_TITLE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                deadline_title,
            )
        ],
        ASK_DESCRIPTION: [
            CommandHandler(
                "skip",
                skip_description,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                deadline_description,
            ),
        ],
        ASK_DATE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                deadline_date,
            )
        ],
        ASK_TIME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                deadline_time,
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