"""
Reminder Callback Handler
-------------------------
Menangani callback untuk Reminder.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services.reminder_service import ReminderService
from services.user_service import UserService
from utils.reminder_formatter import build_reminder_list
from utils.logger import logger

reminder_service = ReminderService()
user_service = UserService()


async def reminder_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    Callback handler Reminder.
    """

    query = update.callback_query
    await query.answer()

    telegram_user = update.effective_user

    db_user = user_service.save_user(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name,
        language_code=telegram_user.language_code,
        is_bot=telegram_user.is_bot,
    )

    data = query.data

    # =====================================================
    # Delete
    # =====================================================

    if data.startswith("reminder_delete_"):

        reminder_id = int(
            data.replace("reminder_delete_", "")
        )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Ya",
                        callback_data=f"reminder_delete_confirm_{reminder_id}",
                    ),
                    InlineKeyboardButton(
                        "❌ Tidak",
                        callback_data="reminder_delete_cancel",
                    ),
                ]
            ]
        )

        await query.edit_message_text(
            "🗑 Hapus reminder ini?",
            reply_markup=keyboard,
        )

        return

    # =====================================================
    # Delete Confirm
    # =====================================================

    if data.startswith("reminder_delete_confirm_"):

        reminder_id = int(
            data.replace(
                "reminder_delete_confirm_",
                "",
            )
        )

        reminder_service.delete_reminder(
            user_id=db_user.id,
            reminder_id=reminder_id,
        )

        reminders = reminder_service.get_reminders(
            user_id=db_user.id,
        )

        text, keyboard = build_reminder_list(reminders)

        logger.info(
            "Reminder deleted | User=%s | Reminder=%s",
            db_user.telegram_id,
            reminder_id,
        )

        await query.edit_message_text(
            text,
            reply_markup=keyboard,
        )

        return

    # =====================================================
    # Delete Cancel
    # =====================================================

    if data == "reminder_delete_cancel":

        reminders = reminder_service.get_reminders(
            user_id=db_user.id,
        )

        text, keyboard = build_reminder_list(reminders)

        await query.edit_message_text(
            text,
            reply_markup=keyboard,
        )

        return

    # =====================================================
    # Edit (Coming Soon)
    # =====================================================

    if data.startswith("reminder_edit_"):

        await query.answer(
            "Fitur Edit Reminder masih dalam pengembangan.",
            show_alert=True,
        )