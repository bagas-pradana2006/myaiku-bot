"""
Start Handler
-------------
Menangani command /start dan /help.
"""

from telegram import Update
from telegram.ext import ContextTypes

from keyboards.main_menu import get_main_menu
from services.user_service import UserService
from utils.logger import logger

user_service = UserService()


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Command /start.
    Menyimpan atau memperbarui data user kemudian
    menampilkan Main Menu.
    """

    telegram_user = update.effective_user

    logger.info(
        "Received /start from %s (%s)",
        telegram_user.first_name,
        telegram_user.id,
    )

    try:
        db_user = user_service.save_user(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            language_code=telegram_user.language_code,
            is_bot=telegram_user.is_bot,
        )

        logger.info(
            "User synchronized successfully: %s",
            db_user.telegram_id,
        )

    except Exception:
        logger.exception("Failed to synchronize user.")

    await update.message.reply_text(
        (
            f"👋 Halo, {telegram_user.first_name}!\n\n"
            "Selamat datang di MyAiku.\n\n"
            "Silakan pilih menu di bawah."
        ),
        reply_markup=get_main_menu(),
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Command /help.
    """

    await update.message.reply_text(
        (
            "📚 Bantuan\n\n"
            "/start - Membuka Main Menu\n"
            "/status - Status server\n"
            "/todo - Tambah Todo (developer)\n"
            "/cancel - Membatalkan proses yang sedang berjalan"
        )
    )