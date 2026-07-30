from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timezone
from models.finance import Finance, TransactionType

class FinanceRepository:
    
    @staticmethod
    def create(session: Session, user_id: int, type: TransactionType, amount: int, category: str, title: str, description: str = None) -> Finance:
        new_transaction = Finance(
            user_id=user_id,
            type=type,
            amount=amount,
            category=category,
            title=title,
            description=description
        )
        session.add(new_transaction)
        session.commit()
        session.refresh(new_transaction)
        return new_transaction

    @staticmethod
    def get_history(session: Session, user_id: int, limit: int = 10) -> list[Finance]:
        return session.query(Finance)\
            .filter(Finance.user_id == user_id)\
            .order_by(Finance.created_at.desc())\
            .limit(limit)\
            .all()

    @staticmethod
    def get_by_id(session: Session, transaction_id: int, user_id: int) -> Finance:
        return session.query(Finance).filter(Finance.id == transaction_id, Finance.user_id == user_id).first()

    @staticmethod
    def delete(session: Session, transaction_id: int, user_id: int) -> bool:
        transaction = FinanceRepository.get_by_id(session, transaction_id, user_id)
        if transaction:
            session.delete(transaction)
            session.commit()
            return True
        return False

    @staticmethod
    def get_summary(session: Session, user_id: int) -> dict:
        """Mengambil total income, expense, dan balance HANYA BULAN INI"""
        now = datetime.now(timezone.utc)
        
        # Hitung Total Income Bulan Ini
        income = session.query(func.sum(Finance.amount)).filter(
            Finance.user_id == user_id, 
            Finance.type == TransactionType.INCOME,
            extract('month', Finance.created_at) == now.month,
            extract('year', Finance.created_at) == now.year
        ).scalar() or 0

        # Hitung Total Expense Bulan Ini
        expense = session.query(func.sum(Finance.amount)).filter(
            Finance.user_id == user_id, 
            Finance.type == TransactionType.EXPENSE,
            extract('month', Finance.created_at) == now.month,
            extract('year', Finance.created_at) == now.year
        ).scalar() or 0

        return {
            "income": income,
            "expense": expense,
            "balance": income - expense
        }