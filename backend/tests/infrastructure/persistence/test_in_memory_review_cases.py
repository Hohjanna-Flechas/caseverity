from datetime import datetime, timezone

from app.domain.review.models import ReviewCase
from app.infrastructure.persistence.in_memory_review_cases import (
    InMemoryReviewCaseRepository,
)


def build_review_case() -> ReviewCase:
    now = datetime.now(timezone.utc)

    return ReviewCase(
        case_id="CASE-0001",
        application_id="APP-0001",
        created_at=now,
        updated_at=now,
    )


def test_repository_saves_and_returns_review_case() -> None:
    repository = InMemoryReviewCaseRepository()
    review_case = build_review_case()

    repository.save(review_case)

    stored_case = repository.get_by_id("CASE-0001")

    assert stored_case is review_case


def test_repository_finds_case_by_application_id() -> None:
    repository = InMemoryReviewCaseRepository()
    review_case = build_review_case()

    repository.save(review_case)

    stored_case = repository.get_by_application_id("APP-0001")

    assert stored_case is review_case


def test_repository_returns_none_when_case_does_not_exist() -> None:
    repository = InMemoryReviewCaseRepository()

    assert repository.get_by_id("UNKNOWN") is None
    assert repository.get_by_application_id("UNKNOWN") is None