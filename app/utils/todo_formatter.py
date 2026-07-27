"""
Todo Formatter
--------------
Utility untuk membuat tampilan Todo List.
"""

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def build_todo_list(todos):
    """
    Membuat text dan inline keyboard Todo List.
    """

    text = "📝 <b>Todo List</b>\n\n"

    keyboard = []

    for index, todo in enumerate(todos, start=1):

        status = "✅" if todo.is_completed else "⏳"

        text += (
            f"{index}. {status} {todo.title}\n"
            "────────────────────\n"
        )

        if todo.is_completed:
            complete_text = "↩️ Batal"
            complete_callback = f"undo_{todo.id}"
        else:
            complete_text = "✅ Selesai"
            complete_callback = f"done_{todo.id}"

        keyboard.append(
            [
                InlineKeyboardButton(
                    complete_text,
                    callback_data=complete_callback,
                ),
                InlineKeyboardButton(
                    "✏ Edit",
                    callback_data=f"edit_{todo.id}",
                ),
            ]
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    "🗑 Hapus",
                    callback_data=f"delete_{todo.id}",
                )
            ]
        )

    text += f"\n📌 Total Todo: {len(todos)}"

    return text, InlineKeyboardMarkup(keyboard)