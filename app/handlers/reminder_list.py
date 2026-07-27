"""
Reminder List Handler
---------------------
Menampilkan daftar reminder milik user.
"""

from telegram import Update
from telegram.ext import ContextTypes

from services.reminder_service import ReminderService
from services.user_service import UserService
from utils.reminder_formatter import build_reminder_list

reminder_service = ReminderService()
user_service = UserService()


async def reminder_list(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    Menampilkan seluruh reminder milik user.
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

    reminders = reminder_service.get_reminders(
        user_id=db_user.id,
    )

    text, keyboard = build_reminder_list(reminders)

    await update.message.reply_text(
        text,
        reply_markup=keyboard,
    )