from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.domain.application.models import CreditApplication


def build_credit_application(**overrides: object) -> CreditApplication:
    data = {
        "application_id": "APP-0001",
        "applicant_id": "SYNTH-0001",
        "created_at": datetime.now(timezone.utc),
        "requested_amount": Decimal("6000.00"),
        "credit_duration_months": 24,
        "credit_purpose": "education",
        "age": 34,
        "employment_status": "employed",
        "employment_duration": "1_to_4_years",
        "existing_credit_count": 1,
        "savings_status": "moderate",
        "installment_commitments": "medium",
        "housing_status": "rent",
        "credit_history": "existing_credit_paid",
        "guarantor_status": "none",
    }

    data.update(overrides)

    return CreditApplication(**data)


def test_credit_application_can_be_created_with_valid_data() -> None:
    application = build_credit_application()

    assert application.application_id == "APP-0001"
    assert application.requested_amount == Decimal("6000.00")
    assert application.age == 34


def test_credit_application_rejects_non_positive_requested_amount() -> None:
    with pytest.raises(
        ValueError,
        match="requested_amount must be greater than zero",
    ):
        build_credit_application(
            requested_amount=Decimal("-500"),
        )

@pytest.mark.parametrize(
    ("field_name", "invalid_value", "expected_message"),
    [
        ("application_id", "", "application_id cannot be empty"),
        ("applicant_id", "", "applicant_id cannot be empty"),
        (
            "credit_duration_months",
            0,
            "credit_duration_months must be greater than zero",
        ),
        ("age", 0, "age must be greater than zero"),
        (
            "existing_credit_count",
            -1,
            "existing_credit_count cannot be negative",
        ),
    ],
)

def test_credit_application_rejects_invalid_domain_values(
    field_name: str,
    invalid_value: object,
    expected_message: str,
) -> None:
    overrides = {
        field_name: invalid_value,
    }

    with pytest.raises(ValueError, match=expected_message):
        build_credit_application(**overrides)