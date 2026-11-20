from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CaseStatus(str, Enum):
    RECEIVED = "received"
    VALIDATED = "validated"
    ASSESSING = "assessing"
    READY_FOR_REVIEW = "ready_for_review"
    MORE_INFORMATION_REQUIRED = "more_information_required"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"


class InvalidCaseTransitionError(Exception):
    pass


_ALLOWED_TRANSITIONS: dict[CaseStatus, set[CaseStatus]] = {
    CaseStatus.RECEIVED: {
        CaseStatus.VALIDATED,
        CaseStatus.FAILED,
    },
    CaseStatus.VALIDATED: {
        CaseStatus.ASSESSING,
        CaseStatus.FAILED,
    },
    CaseStatus.ASSESSING: {
        CaseStatus.READY_FOR_REVIEW,
        CaseStatus.FAILED,
    },
    CaseStatus.READY_FOR_REVIEW: {
        CaseStatus.APPROVED,
        CaseStatus.REJECTED,
        CaseStatus.MORE_INFORMATION_REQUIRED,
    },
    CaseStatus.MORE_INFORMATION_REQUIRED: {
        CaseStatus.VALIDATED,
    },
    CaseStatus.APPROVED: set(),
    CaseStatus.REJECTED: set(),
    CaseStatus.FAILED: set(),
}


@dataclass(slots=True)
class ReviewCase:
    case_id: str
    application_id: str
    created_at: datetime
    updated_at: datetime

    status: CaseStatus = field(
        default=CaseStatus.RECEIVED,
        init=False,
    )

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id cannot be empty")

        if not self.application_id.strip():
            raise ValueError("application_id cannot be empty")

    def transition_to(
        self,
        new_status: CaseStatus,
        occurred_at: datetime,
    ) -> None:
        allowed_transitions = _ALLOWED_TRANSITIONS[self.status]

        if new_status not in allowed_transitions:
            raise InvalidCaseTransitionError(
                f"cannot transition case from "
                f"{self.status.value} to {new_status.value}"
            )

        self.status = new_status
        self.updated_at = occurred_at