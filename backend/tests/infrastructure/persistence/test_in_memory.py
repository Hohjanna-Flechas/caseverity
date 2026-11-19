from datetime import datetime, timezone
from decimal import Decimal

from app.domain.application.models import CreditApplication
from app.infrastructure.persistence.in_memory import (
    InMemoryApplicationRepository,
)


def build_credit_application() -> CreditApplication:
    return CreditApplication(
        application_id="APP-0001",
        applicant_id="SYNTH-0001",
        created_at=datetime.now(timezone.utc),
        requested_amount=Decimal("6000.00"),
        credit_duration_months=24,
        credit_purpose="education",
        age=34,
        employment_status="employed",
        employment_duration="1_to_4_years",
        existing_credit_count=1,
        savings_status="moderate",
        installment_commitments="medium",
        housing_status="rent",
        credit_history="existing_credit_paid",
        guarantor_status="none",
    )


def test_repository_saves_and_returns_application() -> None:
    repository = InMemoryApplicationRepository()
    application = build_credit_application()

    repository.save(application)

    stored_application = repository.get_by_id("APP-0001")

    assert stored_application is application


def test_repository_returns_none_when_application_does_not_exist() -> None:
    repository = InMemoryApplicationRepository()

    assert repository.get_by_id("UNKNOWN") is None