from app.domain.review.models import ReviewCase


class InMemoryReviewCaseRepository:
    def __init__(self) -> None:
        self._cases: dict[str, ReviewCase] = {}

    def save(self, review_case: ReviewCase) -> None:
        self._cases[review_case.case_id] = review_case

    def get_by_id(
        self,
        case_id: str,
    ) -> ReviewCase | None:
        return self._cases.get(case_id)

    def get_by_application_id(
        self,
        application_id: str,
    ) -> ReviewCase | None:
        for review_case in self._cases.values():
            if review_case.application_id == application_id:
                return review_case

        return None