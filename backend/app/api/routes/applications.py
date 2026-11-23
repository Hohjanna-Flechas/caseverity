from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.repositories import (
    get_application_repository,
    get_review_case_repository,
)
from app.api.schemas.applications import (
    CreditApplicationRequest,
    ReviewCaseResponse,
    RiskAssessmentResponse,
    SubmitApplicationResponse,
)
from app.application.repositories.applications import ApplicationRepository
from app.application.repositories.review_cases import ReviewCaseRepository
from app.application.use_cases.submit_application import (
    DuplicateApplicationError,
    SubmitApplication,
)
from app.domain.application.models import CreditApplication
from app.infrastructure.risk.mock import MockRiskService


router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=SubmitApplicationResponse)
def submit_application(
    payload: CreditApplicationRequest,
    application_repository: ApplicationRepository = Depends(
        get_application_repository
    ),
    review_case_repository: ReviewCaseRepository = Depends(
        get_review_case_repository
    ),
) -> SubmitApplicationResponse:
    application = CreditApplication(
        application_id=payload.application_id,
        applicant_id=payload.applicant_id,
        created_at=payload.created_at,
        requested_amount=payload.requested_amount,
        credit_duration_months=payload.credit_duration_months,
        credit_purpose=payload.credit_purpose,
        age=payload.age,
        employment_status=payload.employment_status,
        employment_duration=payload.employment_duration,
        existing_credit_count=payload.existing_credit_count,
        savings_status=payload.savings_status,
        installment_commitments=payload.installment_commitments,
        housing_status=payload.housing_status,
        credit_history=payload.credit_history,
        guarantor_status=payload.guarantor_status,
    )

    use_case = SubmitApplication(
        risk_service=MockRiskService(),
        application_repository=application_repository,
        review_case_repository=review_case_repository,
    )

    try:
        result = use_case.execute(
            application,
            processed_at=datetime.now(timezone.utc),
        )
    except DuplicateApplicationError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return SubmitApplicationResponse(
        application_id=result.application.application_id,
        risk_assessment=RiskAssessmentResponse(
            risk_score=result.risk_assessment.risk_score,
            risk_level=result.risk_assessment.risk_level.value,
            risk_factors=list(result.risk_assessment.risk_factors),
            assessment_source=result.risk_assessment.assessment_source,
            assessed_at=result.risk_assessment.assessed_at,
        ),
        review_case=ReviewCaseResponse(
            case_id=result.review_case.case_id,
            status=result.review_case.status.value,
            created_at=result.review_case.created_at,
            updated_at=result.review_case.updated_at,
        ),
    )