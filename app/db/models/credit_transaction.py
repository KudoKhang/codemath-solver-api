from __future__ import annotations

import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.models.base import Base


class CreditTransaction(Base):
    __tablename__ = "credit_transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    change_amount: Mapped[int] = mapped_column(Integer)
    reason: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    account: Mapped["Account"] = relationship("Account", back_populates="credit_transactions")
