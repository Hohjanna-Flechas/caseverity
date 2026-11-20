import pytest
from datetime import datetime, timezone
from decimal import Decimal

from app.application.use_cases.submit_application import (
    DuplicateApplicationError,
    SubmitApplication,
)
from app.domain.application.models import CreditApplication
from app.domain.risk.models import RiskAssessment, RiskLevel
from app.infrastructure.persistence.in_memory import (
    InMemoryApplicationRepository,
)

from app.domain.review.models import CaseStatus
from app.infrastructure.persistence.in_memory_review_cases import (
    InMemoryReviewCaseRepository,
)


class FakeRiskService:
    def __init__(self) -> None:
        self.received_application: CreditApplication | None = None

    def assess(self, application: CreditApplication) -> RiskAssessment:
        self.received_application = application

        return RiskAssessment(
            application_id=application.application_id,
            risk_score=0.42,
            risk_level=RiskLevel.LOW,
            risk_factors=("test_factor",),
            assessment_source="fake",
            assessed_at=datetime.now(timezone.utc),
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


def test_submit_application_uses_risk_service_and_returns_assessment() -> None:
    application = build_credit_application()

    risk_service = FakeRiskService()
    application_repository = InMemoryApplicationRepository()
    review_case_repository = InMemoryReviewCaseRepository()
    processed_at = datetime.now(timezone.utc)

    use_case = SubmitApplication(
        risk_service=risk_service,
        application_repository=application_repository,
        review_case_repository=review_case_repository,
    )

    result = use_case.execute(
        application,
        processed_at=processed_at,
    )

    assert risk_service.received_application is application

    assert result.application is application
    assert result.risk_assessment.application_id == "APP-0001"
    assert result.risk_assessment.risk_score == 0.42
    assert result.risk_assessment.risk_level is RiskLevel.LOW
    assert result.risk_assessment.assessment_source == "fake"

    assert result.review_case.application_id == "APP-0001"
    assert result.review_case.status is CaseStatus.READY_FOR_REVIEW

    stored_case = review_case_repository.get_by_application_id(
        "APP-0001"
    )

    assert stored_case is result.review_case


def test_submit_application_rejects_duplicate_application() -> None:
    application = build_credit_application()

    risk_service = FakeRiskService()
    application_repository = InMemoryApplicationRepository()
    review_case_repository = InMemoryReviewCaseRepository()
    processed_at = datetime.now(timezone.utc)

    use_case = SubmitApplication(
        risk_service=risk_service,
        application_repository=application_repository,
        review_case_repository=review_case_repository,
    )

    use_case.execute(
        application,
        processed_at=processed_at,
    )

    with pytest.raises(
        DuplicateApplicationError,
        match="application APP-0001 already exists",
    ):
        use_case.execute(
            application,
            processed_at=processed_at,
        )