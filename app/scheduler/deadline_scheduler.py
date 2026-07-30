"""
Deadline Scheduler
------------------
Menjalankan pengecekan deadline secara berkala menggunakan JobQueue.
"""

from telegram.ext import ContextTypes

from services.deadline_service import DeadlineService
from utils.logger import logger

deadline_service = DeadlineService()


async def deadline_scheduler(
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    Mengecek deadline yang sudah waktunya dikirim.
    """

    logger.info("Deadline scheduler running...")

    deadlines = deadline_service.get_pending_deadlines()

    logger.info(
        "Found %d pending deadline(s).",
        len(deadlines),
    )

    for deadline in deadlines:
        try:
            logger.info(
                "Sending deadline | User=%s | Deadline=%s",
                deadline.user.telegram_id,
                deadline.id,
            )

            priority = deadline.priority or "-"

            await context.bot.send_message(
                chat_id=deadline.user.telegram_id,
                text=(
                    "📅 Deadline\n\n"
                    f"📌 {deadline.title}\n"
                    f"📝 {deadline.description or '-'}\n"
                    f"🔥 Priority : {priority}"
                ),
            )

            deadline_service.mark_as_notified(
                deadline.id,
            )

            logger.info(
                "Deadline sent | User=%s | Deadline=%s",
                deadline.user.telegram_id,
                deadline.id,
            )

        except Exception:
            logger.exception(
                "Failed to send deadline %s",
                deadline.id,
            )