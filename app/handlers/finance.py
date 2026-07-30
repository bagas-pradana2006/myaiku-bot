"""
Finance Conversation Handler
----------------------------
Menangani alur percakapan (Conversation) untuk menambah Income & Expense.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from handlers.finance_list import finance_list
from models.finance import TransactionType
from services.finance_service import FinanceService
from services.user_service import UserService

# State percakapan
AMOUNT, CATEGORY, TITLE = range(3)

user_service = UserService()
finance_service = FinanceService()

async def start_add_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Mulai percakapan menambah transaksi."""
    query = update.callback_query
    await query.answer()

    # Cek apakah income atau expense dari callback data
    is_income = "add_income" in query.data
    tx_type = TransactionType.INCOME if is_income else TransactionType.EXPENSE
    
    # Simpan tipe transaksi di memori sementara
    context.user_data["tx_type"] = tx_type

    tipe_teks = "Pemasukan 🟢" if is_income else "Pengeluaran 🔴"
    
    await query.edit_message_text(
        f"Kamu akan menambah *{tipe_teks}*\n\n"
        "Berapa nominalnya? (Ketik angkanya saja, contoh: 50000)\n\n"
        "Ketik /cancel untuk membatalkan.",
        parse_mode="Markdown"
    )
    return AMOUNT

async def receive_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Menerima nominal uang."""
    text = update.message.text.strip()
    
    # Validasi hanya angka
    if not text.isdigit():
        await update.message.reply_text(
            "❌ Format salah! Harap masukkan angka saja (contoh: 50000).\n"
            "Silakan ketik ulang nominalnya:"
        )
        return AMOUNT

    context.user_data["amount"] = int(text)
    tx_type = context.user_data["tx_type"]

    # Siapkan kategori sesuai tipe transaksi
    if tx_type == TransactionType.INCOME:
        categories = ["Gaji", "Bonus", "Investasi", "Hadiah", "Lainnya"]
    else:
        categories = ["Makanan", "Transport", "Belanja", "Tagihan", "Hiburan", "Lainnya"]

    # Buat tombol kategori
    keyboard = []
    # Susun tombol 2 kolom
    for i in range(0, len(categories), 2):
        row = [InlineKeyboardButton(cat, callback_data=f"cat_{cat}") for cat in categories[i:i+2]]
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Pilih kategori transaksinya:",
        reply_markup=reply_markup
    )
    return CATEGORY

async def receive_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Menerima kategori dari tombol."""
    query = update.callback_query
    await query.answer()
    
    # Ambil nama kategori (hilangkan prefix 'cat_')
    category = query.data.replace("cat_", "")
    context.user_data["category"] = category

    await query.edit_message_text(
        f"Kategori *{category}* dipilih.\n\n"
        "Masukkan keterangan singkat:\n"
        "(Contoh: Gaji bulan Januari / Beli kopi)",
        parse_mode="Markdown"
    )
    return TITLE

async def receive_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Menerima keterangan dan menyimpan ke database."""
    title = update.message.text.strip()
    
    # Ambil data dari temporary storage
    tx_type = context.user_data["tx_type"]
    amount = context.user_data["amount"]
    category = context.user_data["category"]
    
    telegram_user = update.effective_user
    db_user = user_service.get_user_by_telegram_id(telegram_user.id)

    if not db_user:
        await update.message.reply_text("❌ Terjadi kesalahan: User tidak ditemukan.")
        return ConversationHandler.END

    # Simpan ke database
    finance_service.add_transaction(
        user_id=db_user.id,
        tx_type=tx_type,
        amount=amount,
        category=category,
        title=title
    )

    # Bersihkan memori sementara
    context.user_data.pop("tx_type", None)
    context.user_data.pop("amount", None)
    context.user_data.pop("category", None)

    # Beri pesan sukses
    await update.message.reply_text("✅ Transaksi berhasil dicatat!")
    
    # Tampilkan kembali dashboard
    await finance_list(update, context)

    return ConversationHandler.END

async def cancel_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Membatalkan penambahan transaksi."""
    context.user_data.pop("tx_type", None)
    context.user_data.pop("amount", None)
    context.user_data.pop("category", None)
    
    await update.message.reply_text("🚫 Transaksi dibatalkan.")
    await finance_list(update, context)
    return ConversationHandler.END

# Konfigurasi Conversation Handler
finance_conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_add_transaction, pattern="^finance_add_(income|expense)$")
    ],
    states={
        AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_amount)],
        CATEGORY: [CallbackQueryHandler(receive_category, pattern="^cat_")],
        TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_title)],
    },
    fallbacks=[CommandHandler("cancel", cancel_transaction)],
)