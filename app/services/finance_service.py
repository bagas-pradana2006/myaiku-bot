from database.session import SessionLocal
from models.finance import TransactionType
from repositories.finance_repository import FinanceRepository

class FinanceService:
    
    @staticmethod
    def format_rupiah(amount: int) -> str:
        return f"Rp {amount:,.0f}".replace(",", ".")

    @staticmethod
    def add_transaction(user_id: int, tx_type: TransactionType, amount: int, category: str, title: str, description: str = None):
        with SessionLocal() as db:
            return FinanceRepository.create(db, user_id, tx_type, amount, category, title, description)

    @staticmethod
    def get_summary_text(user_id: int) -> str:
        with SessionLocal() as db:
            summary = FinanceRepository.get_summary(db, user_id)
        
        income = FinanceService.format_rupiah(summary["income"])
        expense = FinanceService.format_rupiah(summary["expense"])
        balance = FinanceService.format_rupiah(summary["balance"])

        balance_icon = "🟢" if summary["balance"] >= 0 else "🔴"

        text = (
            "📊 *Ringkasan Keuangan (Bulan Ini)*\n\n"
            f"📈 *Pemasukan:* {income}\n"
            f"📉 *Pengeluaran:* {expense}\n"
            "──────────────\n"
            f"{balance_icon} *Saldo Aktif:* {balance}"
        )
        return text

    @staticmethod
    def get_history_data(user_id: int, limit: int = 5) -> list:
        """Mengambil data mentah untuk dibuatkan tombol Hapus di Handler"""
        with SessionLocal() as db:
            return FinanceRepository.get_history(db, user_id, limit)

    @staticmethod
    def get_history_text(history: list) -> str:
        if not history:
            return "Belum ada catatan transaksi. Yuk, mulai catat keuanganmu! 💸"
        
        text = "📝 *Histori Transaksi Terakhir*\n\n"
        for tx in history:
            icon = "🟢" if tx.type == TransactionType.INCOME else "🔴"
            amount_str = FinanceService.format_rupiah(tx.amount)
            date_str = tx.created_at.strftime("%d %b %Y %H:%M")
            
            text += f"{icon} *{tx.title}* ({tx.category})\n"
            text += f"💵 {amount_str}  |  📅 {date_str}\n\n"
            
        return text
        
    @staticmethod
    def delete_transaction(transaction_id: int, user_id: int) -> bool:
        with SessionLocal() as db:
            return FinanceRepository.delete(db, transaction_id, user_id)