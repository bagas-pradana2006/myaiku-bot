import logging

from telegram import Update
from telegram.ext import ContextTypes

from services.user_service import UserService

logger = logging.getLogger(__name__)

user_service = UserService()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    logger.info(
        "Received /start from %s (%s)",
        user.first_name,
        user.id,
    )

    try:
        saved_user = user_service.save_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
        )

        logger.info(
            "User saved successfully: %s",
            saved_user.telegram_id,
        )

    except Exception:
        logger.exception("Failed to save user")

    await update.message.reply_text(
        f"👋 Halo, {user.first_name}!\n\n"
        "Saya MyAiku Bot v3.\n\n"
        "✅ Server berjalan dengan baik."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Daftar Perintah\n\n"
        "/start - Memulai bot\n"
        "/help - Bantuan"
    )