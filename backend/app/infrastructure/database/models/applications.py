from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class CreditApplicationRecord(Base):
    __tablename__ = "credit_applications"

    application_id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
    )
    applicant_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    requested_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )
    credit_duration_months: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    credit_purpose: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    employment_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    employment_duration: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    existing_credit_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    savings_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    installment_commitments: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    housing_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    credit_history: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    guarantor_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )