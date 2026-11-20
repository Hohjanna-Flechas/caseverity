from datetime import datetime, timezone

import pytest

from app.domain.review.models import (
    CaseStatus,
    InvalidCaseTransitionError,
    ReviewCase,
)


def build_review_case() -> ReviewCase:
    now = datetime.now(timezone.utc)

    return ReviewCase(
        case_id="CASE-0001",
        application_id="APP-0001",
        created_at=now,
        updated_at=now,
    )


def test_review_case_starts_as_received() -> None:
    case = build_review_case()

    assert case.status is CaseStatus.RECEIVED


def test_review_case_can_follow_happy_path_to_approved() -> None:
    case = build_review_case()

    case.transition_to(
        CaseStatus.VALIDATED,
        occurred_at=datetime.now(timezone.utc),
    )
    case.transition_to(
        CaseStatus.ASSESSING,
        occurred_at=datetime.now(timezone.utc),
    )
    case.transition_to(
        CaseStatus.READY_FOR_REVIEW,
        occurred_at=datetime.now(timezone.utc),
    )
    case.transition_to(
        CaseStatus.APPROVED,
        occurred_at=datetime.now(timezone.utc),
    )

    assert case.status is CaseStatus.APPROVED


def test_review_case_rejects_invalid_transition() -> None:
    case = build_review_case()

    with pytest.raises(
        InvalidCaseTransitionError,
        match="cannot transition case from received to approved",
    ):
        case.transition_to(
            CaseStatus.APPROVED,
            occurred_at=datetime.now(timezone.utc),
        )


@pytest.mark.parametrize(
    "terminal_status",
    [
        CaseStatus.APPROVED,
        CaseStatus.REJECTED,
    ],
)
def test_terminal_states_do_not_allow_further_transitions(
    terminal_status: CaseStatus,
) -> None:
    case = build_review_case()

    case.transition_to(
        CaseStatus.VALIDATED,
        occurred_at=datetime.now(timezone.utc),
    )
    case.transition_to(
        CaseStatus.ASSESSING,
        occurred_at=datetime.now(timezone.utc),
    )
    case.transition_to(
        CaseStatus.READY_FOR_REVIEW,
        occurred_at=datetime.now(timezone.utc),
    )
    case.transition_to(
        terminal_status,
        occurred_at=datetime.now(timezone.utc),
    )

    with pytest.raises(InvalidCaseTransitionError):
        case.transition_to(
            CaseStatus.VALIDATED,
            occurred_at=datetime.now(timezone.utc),
        )


def test_more_information_required_can_return_to_validated() -> None:
    case = build_review_case()

    case.transition_to(
        CaseStatus.VALIDATED,
        occurred_at=datetime.now(timezone.utc),
    )
    case.transition_to(
        CaseStatus.ASSESSING,
        occurred_at=datetime.now(timezone.utc),
    )
    case.transition_to(
        CaseStatus.READY_FOR_REVIEW,
        occurred_at=datetime.now(timezone.utc),
    )
    case.transition_to(
        CaseStatus.MORE_INFORMATION_REQUIRED,
        occurred_at=datetime.now(timezone.utc),
    )
    case.transition_to(
        CaseStatus.VALIDATED,
        occurred_at=datetime.now(timezone.utc),
    )

    assert case.status is CaseStatus.VALIDATED