"""
Reminder Formatter
------------------
Utilities untuk memformat daftar Reminder.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from models.reminder import Reminder
from utils.time import utc_to_wib


def build_reminder_list(
    reminders: list[Reminder],
) -> tuple[str, InlineKeyboardMarkup]:
    """
    Membuat teks dan inline keyboard daftar reminder.
    """

    if not reminders:
        return (
            "⏰ Belum ada reminder.",
            InlineKeyboardMarkup([]),
        )

    lines: list[str] = [
        "⏰ Reminder List",
        "",
    ]

    keyboard: list[list[InlineKeyboardButton]] = []

    for index, reminder in enumerate(reminders, start=1):
        remind_at = utc_to_wib(
            reminder.remind_at,
        ).strftime("%d-%m-%Y %H:%M")

        lines.append(
            f"{index}. ⏰ {reminder.title}"
        )
        lines.append(
            f"📅 {remind_at}"
        )
        lines.append("")

        keyboard.append(
            [
                InlineKeyboardButton(
                    "✏ Edit",
                    callback_data=f"reminder_edit_{reminder.id}",
                ),
                InlineKeyboardButton(
                    "🗑 Hapus",
                    callback_data=f"reminder_delete_{reminder.id}",
                ),
            ]
        )

    lines.append(f"📌 Total Reminder: {len(reminders)}")

    return (
        "\n".join(lines),
        InlineKeyboardMarkup(keyboard),
    )