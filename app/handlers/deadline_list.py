"""
Deadline List Handler
---------------------
Menampilkan seluruh deadline milik user.
"""

from telegram import Update
from telegram.ext import ContextTypes

from services.deadline_service import DeadlineService
from services.user_service import UserService
from utils.deadline_formatter import build_deadline_list
from utils.logger import logger

deadline_service = DeadlineService()
user_service = UserService()


async def deadline_list(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    Menampilkan seluruh deadline milik user.
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

    deadlines = deadline_service.get_deadlines(
        user_id=db_user.id,
    )

    if not deadlines:

        await update.message.reply_text(
            "📅 Kamu belum memiliki Deadline."
        )

        logger.info(
            "Deadline list requested | User=%s | Total=0",
            db_user.telegram_id,
        )

        return

    text, keyboard = build_deadline_list(
        deadlines,
    )

    logger.info(
        "Deadline list requested | User=%s | Total=%s",
        db_user.telegram_id,
        len(deadlines),
    )

    await update.message.reply_text(
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )