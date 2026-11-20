from typing import Protocol

from app.domain.review.models import ReviewCase


class ReviewCaseRepository(Protocol):
    def save(self, review_case: ReviewCase) -> None:
        ...

    def get_by_id(
        self,
        case_id: str,
    ) -> ReviewCase | None:
        ...

    def get_by_application_id(
        self,
        application_id: str,
    ) -> ReviewCase | None:
        ...