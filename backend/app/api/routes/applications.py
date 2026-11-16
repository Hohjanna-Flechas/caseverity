from fastapi import APIRouter

from app.api.schemas.applications import (
    CreditApplicationRequest,
    RiskAssessmentResponse,
    SubmitApplicationResponse,
)
from app.application.use_cases.submit_application import SubmitApplication
from app.domain.application.models import CreditApplication
from app.infrastructure.risk.mock import MockRiskService


router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=SubmitApplicationResponse)
def submit_application(
    payload: CreditApplicationRequest,
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
    )

    result = use_case.execute(application)

    return SubmitApplicationResponse(
        application_id=result.application.application_id,
        risk_assessment=RiskAssessmentResponse(
            risk_score=result.risk_assessment.risk_score,
            risk_level=result.risk_assessment.risk_level.value,
            risk_factors=list(result.risk_assessment.risk_factors),
            assessment_source=result.risk_assessment.assessment_source,
            assessed_at=result.risk_assessment.assessed_at,
        ),
    )
