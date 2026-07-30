"""
Deadline Callback Handler
-------------------------
Menangani seluruh callback Deadline.
"""

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from services.deadline_service import DeadlineService
from services.user_service import UserService
from utils.deadline_formatter import build_deadline_list
from utils.logger import logger

deadline_service = DeadlineService()
user_service = UserService()


async def refresh_deadline_list(query, user_id: int):
    """Refresh tampilan deadline."""

    deadlines = deadline_service.get_deadlines(user_id)

    if not deadlines:
        await query.edit_message_text(
            "📅 Kamu belum memiliki Deadline."
        )
        return

    text, keyboard = build_deadline_list(deadlines)

    await query.edit_message_text(
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


async def deadline_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query
    await query.answer()

    data = query.data

    logger.info(
        "Deadline callback received: %s",
        data,
    )

    telegram_user = update.effective_user

    db_user = user_service.get_user_by_telegram_id(
        telegram_user.id,
    )

    if not db_user:
        await query.answer(
            "User tidak ditemukan.",
            show_alert=True,
        )
        return

    # ==========================================
    # COMPLETE
    # ==========================================

    if data.startswith("deadline_done_"):

        deadline_id = int(data.split("_")[2])

        deadline = deadline_service.complete_deadline(
            db_user.id,
            deadline_id,
        )

        if not deadline:
            await query.answer(
                "Deadline tidak ditemukan.",
                show_alert=True,
            )
            return

        await refresh_deadline_list(
            query,
            db_user.id,
        )

        return

    # ==========================================
    # UNDO
    # ==========================================

    if data.startswith("deadline_undo_"):

        deadline_id = int(data.split("_")[2])

        deadline = deadline_service.uncomplete_deadline(
            db_user.id,
            deadline_id,
        )

        if not deadline:
            await query.answer(
                "Deadline tidak ditemukan.",
                show_alert=True,
            )
            return

        await refresh_deadline_list(
            query,
            db_user.id,
        )

        return

    # ==========================================
    # DELETE CONFIRM
    # ==========================================

    if data.startswith("deadline_delete_confirm_"):

        deadline_id = int(data.split("_")[3])

        deadline_service.delete_deadline(
            db_user.id,
            deadline_id,
        )

        await refresh_deadline_list(
            query,
            db_user.id,
        )

        return

    # ==========================================
    # DELETE CANCEL
    # ==========================================

    if data == "deadline_delete_cancel":

        await refresh_deadline_list(
            query,
            db_user.id,
        )

        return

    # ==========================================
    # DELETE
    # ==========================================

    if data.startswith("deadline_delete_"):

        deadline_id = int(data.split("_")[2])

        deadline = deadline_service.get_deadline(
            db_user.id,
            deadline_id,
        )

        if not deadline:
            await query.answer(
                "Deadline tidak ditemukan.",
                show_alert=True,
            )
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Ya, Hapus",
                        callback_data=f"deadline_delete_confirm_{deadline.id}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❌ Batal",
                        callback_data="deadline_delete_cancel",
                    )
                ],
            ]
        )

        await query.edit_message_text(
            text=(
                "⚠️ <b>Konfirmasi Hapus</b>\n\n"
                f"📅 {deadline.title}\n\n"
                "Yakin ingin menghapus deadline ini?"
            ),
            parse_mode="HTML",
            reply_markup=keyboard,
        )

        return

    # ==========================================
    # EDIT
    # ==========================================

    if data.startswith("deadline_edit_"):

        await query.answer(
            "✏️ Edit Deadline (Coming Soon)",
            show_alert=False,
        )

        return

    # ==========================================
    # UNKNOWN
    # ==========================================

    await query.answer(
        "Callback tidak dikenali.",
        show_alert=True,
    )