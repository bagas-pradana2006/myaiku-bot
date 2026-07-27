"""
Menu Handler
------------
Menangani navigasi menu utama MyAiku.
"""

from telegram import Update
from telegram.ext import ContextTypes

from keyboards.main_menu import get_main_menu


async def back_to_main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Kembali ke menu utama."""

    await update.message.reply_text(
        "🏠 Main Menu\n\nSilakan pilih menu.",
        reply_markup=get_main_menu(),
    )