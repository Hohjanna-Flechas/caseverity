from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class ReviewCaseRecord(Base):
    __tablename__ = "review_cases"

    case_id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
    )

    application_id: Mapped[str] = mapped_column(
        ForeignKey("credit_applications.application_id"),
        unique=True,
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )