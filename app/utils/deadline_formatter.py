"""
Deadline Formatter
------------------
Formatter untuk menampilkan daftar deadline.
"""

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from utils.time import utc_to_wib


def build_deadline_list(deadlines):
    """
    Membangun tampilan daftar deadline.
    """

    if not deadlines:
        return (
            "📅 <b>Daftar Deadline</b>\n\n"
            "Belum ada deadline.",
            None,
        )

    lines = [
        "📅 <b>Daftar Deadline</b>",
        "",
    ]

    keyboard = []

    for deadline in deadlines:

        icon = "🟢" if deadline.is_completed else "🔴"

        deadline_time = utc_to_wib(
            deadline.deadline_at,
        ).strftime("%d-%m-%Y %H:%M WIB")

        lines.extend(
            [
                f"{icon} <b>{deadline.title}</b>",
                f"🗓 {deadline_time}",
                f"⭐ Priority : {deadline.priority}",
            ]
        )

        if deadline.description:
            lines.append(
                f"📝 {deadline.description}"
            )

        lines.append("")

        # ==========================================
        # Action Button
        # ==========================================

        if deadline.is_completed:
            action_button = InlineKeyboardButton(
                "↩️",
                callback_data=f"deadline_undo_{deadline.id}",
            )
        else:
            action_button = InlineKeyboardButton(
                "✅",
                callback_data=f"deadline_done_{deadline.id}",
            )

        keyboard.append(
            [
                action_button,
                InlineKeyboardButton(
                    "✏️",
                    callback_data=f"deadline_edit_{deadline.id}",
                ),
                InlineKeyboardButton(
                    "🗑️",
                    callback_data=f"deadline_delete_{deadline.id}",
                ),
            ]
        )

    return (
        "\n".join(lines),
        InlineKeyboardMarkup(keyboard),
    )