import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.exception(
        "Unhandled exception",
        exc_info=context.error,
    )

    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Terjadi kesalahan.\n\n"
            "Silakan coba lagi beberapa saat."
        )