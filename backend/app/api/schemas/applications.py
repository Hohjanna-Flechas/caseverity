from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class CreditApplicationRequest(BaseModel):
    application_id: str = Field(min_length=1)
    applicant_id: str = Field(min_length=1)
    created_at: datetime

    requested_amount: Decimal = Field(gt=0)
    credit_duration_months: int = Field(gt=0)
    credit_purpose: str = Field(min_length=1)

    age: int = Field(gt=0)
    employment_status: str = Field(min_length=1)
    employment_duration: str = Field(min_length=1)

    existing_credit_count: int = Field(ge=0)
    savings_status: str = Field(min_length=1)
    installment_commitments: str = Field(min_length=1)
    housing_status: str = Field(min_length=1)

    credit_history: str = Field(min_length=1)
    guarantor_status: str = Field(min_length=1)


class RiskAssessmentResponse(BaseModel):
    risk_score: float
    risk_level: str
    risk_factors: list[str]
    assessment_source: str
    assessed_at: datetime


class ReviewCaseResponse(BaseModel):
    case_id: str
    status: str
    created_at: datetime
    updated_at: datetime


class SubmitApplicationResponse(BaseModel):
    application_id: str
    risk_assessment: RiskAssessmentResponse
    review_case: ReviewCaseResponse