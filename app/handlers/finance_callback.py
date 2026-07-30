from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from handlers.finance_list import finance_list
from models.finance import TransactionType
from services.finance_service import FinanceService
from services.user_service import UserService

user_service = UserService()

async def finance_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    telegram_id = update.effective_user.id
    
    db_user = user_service.get_user_by_telegram_id(telegram_id)
    if not db_user:
        return

    # --- 1. MENU HISTORI ---
    if data == "finance_history":
        history = FinanceService.get_history_data(db_user.id, limit=5)
        text = FinanceService.get_history_text(history)
        
        keyboard = []
        # Tambahkan tombol Hapus untuk masing-masing transaksi
        for tx in history:
            icon = "🟢" if tx.type == TransactionType.INCOME else "🔴"
            keyboard.append([InlineKeyboardButton(f"❌ Hapus {icon} {tx.title}", callback_data=f"finance_del_{tx.id}")])
            
        keyboard.append([InlineKeyboardButton("⬅️ Kembali ke Dashboard", callback_data="finance_summary")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")
        
    # --- 2. KONFIRMASI HAPUS ---
    elif data.startswith("finance_del_"):
        tx_id = int(data.split("_")[2])
        keyboard = [
            [
                InlineKeyboardButton("✅ Ya, Hapus", callback_data=f"finance_delconfirm_{tx_id}"),
                InlineKeyboardButton("🚫 Batal", callback_data="finance_history")
            ]
        ]
        await query.edit_message_text(
            "⚠️ *Yakin ingin menghapus transaksi ini?*\n\nData yang dihapus akan mengubah saldo dan tidak bisa dikembalikan.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        
    # --- 3. EKSEKUSI HAPUS ---
    elif data.startswith("finance_delconfirm_"):
        tx_id = int(data.split("_")[2])
        FinanceService.delete_transaction(tx_id, db_user.id)
        
        # Kembali ke dashboard
        await finance_list(update, context)

    # --- 4. KEMBALI KE DASHBOARD ---
    elif data == "finance_summary":
        await finance_list(update, context)