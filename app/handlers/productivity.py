from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from utils.logger import logger

productivity_keyboard = ReplyKeyboardMarkup(
    [
        ["📝 Todo", "⏰ Reminder"],
        ["📅 Deadline", "📝 Notes"],
        ["⬅️ Kembali"],
    ],
    resize_keyboard=True,
)


async def productivity_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(
        "PRODUCTIVITY CALLBACK CALLED: %s",
        update.message.text,
    )

    await update.message.reply_text(
        "INI PRODUCTIVITY",
        reply_markup=productivity_keyboard,
    )