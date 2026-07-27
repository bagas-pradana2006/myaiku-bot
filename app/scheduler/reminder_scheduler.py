"""
Reminder Scheduler
------------------
Menjalankan pengecekan reminder secara berkala menggunakan JobQueue.
"""

from telegram.ext import ContextTypes

from services.reminder_service import ReminderService
from utils.logger import logger

reminder_service = ReminderService()


async def reminder_scheduler(
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    Mengecek reminder yang sudah waktunya dikirim.
    """

    logger.info("Reminder scheduler running...")

    reminders = reminder_service.get_pending_reminders()

    logger.info(
        "Found %d pending reminder(s).",
        len(reminders),
    )

    for reminder in reminders:
        try:
            logger.info(
                "Sending reminder | User=%s | Reminder=%s",
                reminder.user.telegram_id,
                reminder.id,
            )

            await context.bot.send_message(
                chat_id=reminder.user.telegram_id,
                text=(
                    "⏰ Reminder\n\n"
                    f"📝 {reminder.title}"
                ),
            )

            reminder_service.mark_as_sent(
                reminder.id,
            )

            logger.info(
                "Reminder sent | User=%s | Reminder=%s",
                reminder.user.telegram_id,
                reminder.id,
            )

        except Exception:
            logger.exception(
                "Failed to send reminder %s",
                reminder.id,
            )