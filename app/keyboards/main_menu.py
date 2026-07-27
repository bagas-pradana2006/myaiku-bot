"""
Main Menu Keyboard
"""

from telegram import ReplyKeyboardMarkup


def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        ["📋 Productivity", "💰 Finance"],
        ["🛠 Utilities", "📁 File Tools"],
        ["🌤 Information", "⚙ Settings"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )