"""
Global Error Handler
--------------------
Menangani seluruh exception yang tidak tertangani pada Telegram Bot.
"""

from telegram import Update
from telegram.ext import ContextTypes

from utils.logger import logger


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Global error handler."""

    logger.exception(
        "Unhandled exception occurred.",
        exc_info=context.error,
    )

    if not isinstance(update, Update):
        return

    user = update.effective_user
    chat = update.effective_chat

    logger.error(
        "User=%s | Chat=%s | Error=%s",
        user.id if user else "-",
        chat.id if chat else "-",
        type(context.error).__name__,
    )

    try:
        if update.callback_query:
            await update.callback_query.answer(
                "❌ Terjadi kesalahan pada sistem.",
                show_alert=True,
            )
        elif update.effective_message:
            await update.effective_message.reply_text(
                "❌ Terjadi kesalahan pada sistem.\n\n"
                "Silakan coba beberapa saat lagi."
            )
    except Exception:
        logger.exception("Failed to send error message to user.")