"""
Finance List Handler
--------------------
Menampilkan ringkasan keuangan (Summary) dan menu inline keyboard.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services.finance_service import FinanceService
from services.user_service import UserService

user_service = UserService()

async def finance_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menampilkan dashboard keuangan pengguna."""
    telegram_id = update.effective_user.id
    
    # Konversi ID Telegram ke ID Database Internal
    db_user = user_service.get_user_by_telegram_id(telegram_id)
    if not db_user:
        return

    # Ambil teks summary dari Service menggunakan ID Internal
    text = FinanceService.get_summary_text(db_user.id)

    # Buat tombol inline
    keyboard = [
        [
            InlineKeyboardButton("➕ Pemasukan", callback_data="finance_add_income"),
            InlineKeyboardButton("➖ Pengeluaran", callback_data="finance_add_expense"),
        ],
        [
            InlineKeyboardButton("📜 Histori Transaksi", callback_data="finance_history")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Kirim pesan (bisa dari command /finance atau callback navigasi)
    if update.message:
        await update.message.reply_text(
            text, 
            reply_markup=reply_markup, 
            parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text, 
            reply_markup=reply_markup, 
            parse_mode="Markdown"
        )