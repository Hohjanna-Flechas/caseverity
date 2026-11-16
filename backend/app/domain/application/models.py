from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True)
class CreditApplication:
    application_id: str
    applicant_id: str
    created_at: datetime

    requested_amount: Decimal
    credit_duration_months: int
    credit_purpose: str

    age: int
    employment_status: str
    employment_duration: str

    existing_credit_count: int
    savings_status: str
    installment_commitments: str
    housing_status: str

    credit_history: str
    guarantor_status: str

    def __post_init__(self) -> None:
        if not self.application_id.strip():
            raise ValueError("application_id cannot be empty")

        if not self.applicant_id.strip():
            raise ValueError("applicant_id cannot be empty")

        if self.requested_amount <= 0:
            raise ValueError("requested_amount must be greater than zero")

        if self.credit_duration_months <= 0:
            raise ValueError("credit_duration_months must be greater than zero")

        if self.age <= 0:
            raise ValueError("age must be greater than zero")

        if self.existing_credit_count < 0:
            raise ValueError("existing_credit_count cannot be negative")