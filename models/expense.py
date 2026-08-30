from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Column, Date, DateTime, Index, Integer, Numeric, String, Text

from extensions import db


_EXPENSE_TABLE_READY_FOR = None


class Expense(db.Model):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    category = Column(String(120), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    incurred_on = Column(Date, nullable=False, default=date.today, index=True)
    notes = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_expenses_incurred_category", "incurred_on", "category"),
        Index("idx_expenses_created_at", "created_at"),
    )

    @property
    def amount_label(self):
        return f"{Decimal(self.amount or 0):,.2f}"


def ensure_expense_table():
    """Ensure the additive expense table exists on the configured database.

    Expenses were introduced after some production databases were created.  The
    check-first DDL is idempotent, so running it during the first request on a
    cold worker safely upgrades those databases without a separate migration
    framework.
    """
    global _EXPENSE_TABLE_READY_FOR

    database_key = str(db.engine.url)
    if _EXPENSE_TABLE_READY_FOR == database_key:
        return

    Expense.__table__.create(bind=db.engine, checkfirst=True)
    for index in Expense.__table__.indexes:
        index.create(bind=db.engine, checkfirst=True)

    _EXPENSE_TABLE_READY_FOR = database_key
