from datetime import datetime, timezone

import pytest

from app.domain.risk.models import RiskAssessment, RiskLevel


def build_risk_assessment(**overrides: object) -> RiskAssessment:
    data = {
        "application_id": "APP-0001",
        "risk_score": 0.64,
        "risk_level": RiskLevel.MEDIUM,
        "risk_factors": (
            "recent_credit_history",
            "existing_credit_commitments",
        ),
        "assessment_source": "mock",
        "assessed_at": datetime.now(timezone.utc),
    }

    data.update(overrides)

    return RiskAssessment(**data)


def test_risk_assessment_can_be_created_with_valid_data() -> None:
    assessment = build_risk_assessment()

    assert assessment.application_id == "APP-0001"
    assert assessment.risk_score == 0.64
    assert assessment.risk_level is RiskLevel.MEDIUM
    assert assessment.assessment_source == "mock"


@pytest.mark.parametrize(
    "invalid_score",
    [-0.01, 1.01],
)

def test_risk_assessment_rejects_score_outside_valid_range(
    invalid_score: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="risk_score must be between 0 and 1",
    ):
        build_risk_assessment(
            risk_score=invalid_score,
        )


@pytest.mark.parametrize(
    ("field_name", "invalid_value", "expected_message"),
    [
        (
            "application_id",
            "",
            "application_id cannot be empty",
        ),
        (
            "assessment_source",
            "",
            "assessment_source cannot be empty",
        ),
    ],
)

def test_risk_assessment_rejects_invalid_required_values(
    field_name: str,
    invalid_value: object,
    expected_message: str,
) -> None:
    overrides = {
        field_name: invalid_value,
    }

    with pytest.raises(ValueError, match=expected_message):
        build_risk_assessment(**overrides)