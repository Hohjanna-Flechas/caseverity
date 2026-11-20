from dataclasses import dataclass
from datetime import datetime

from app.application.repositories.applications import ApplicationRepository
from app.application.repositories.review_cases import ReviewCaseRepository
from app.domain.application.models import CreditApplication
from app.domain.review.models import CaseStatus, ReviewCase
from app.domain.risk.models import RiskAssessment
from app.domain.risk.services import RiskService


class DuplicateApplicationError(Exception):
    pass


@dataclass(slots=True)
class SubmitApplicationResult:
    application: CreditApplication
    risk_assessment: RiskAssessment
    review_case: ReviewCase


class SubmitApplication:
    def __init__(
        self,
        risk_service: RiskService,
        application_repository: ApplicationRepository,
        review_case_repository: ReviewCaseRepository,
    ) -> None:
        self._risk_service = risk_service
        self._application_repository = application_repository
        self._review_case_repository = review_case_repository

    def execute(
        self,
        application: CreditApplication,
        processed_at: datetime,
    ) -> SubmitApplicationResult:
        existing_application = self._application_repository.get_by_id(
            application.application_id
        )

        if existing_application is not None:
            raise DuplicateApplicationError(
                f"application {application.application_id} already exists"
            )

        self._application_repository.save(application)

        review_case = ReviewCase(
            case_id=f"CASE-{application.application_id}",
            application_id=application.application_id,
            created_at=processed_at,
            updated_at=processed_at,
        )

        self._review_case_repository.save(review_case)

        review_case.transition_to(
            CaseStatus.VALIDATED,
            occurred_at=processed_at,
        )
        self._review_case_repository.save(review_case)

        review_case.transition_to(
            CaseStatus.ASSESSING,
            occurred_at=processed_at,
        )
        self._review_case_repository.save(review_case)

        risk_assessment = self._risk_service.assess(application)

        review_case.transition_to(
            CaseStatus.READY_FOR_REVIEW,
            occurred_at=processed_at,
        )
        self._review_case_repository.save(review_case)

        return SubmitApplicationResult(
            application=application,
            risk_assessment=risk_assessment,
            review_case=review_case,
        )