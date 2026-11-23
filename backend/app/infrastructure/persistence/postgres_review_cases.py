from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.domain.review.models import CaseStatus, ReviewCase
from app.infrastructure.database.models.review_cases import ReviewCaseRecord


class PostgresReviewCaseRepository:
    def __init__(
        self,
        session_factory: sessionmaker[Session],
    ) -> None:
        self._session_factory = session_factory

    def save(
        self,
        review_case: ReviewCase,
    ) -> None:
        with self._session_factory() as session:
            existing_record = session.get(
                ReviewCaseRecord,
                review_case.case_id,
            )

            if existing_record is None:
                session.add(self._to_record(review_case))
            else:
                existing_record.status = review_case.status.value
                existing_record.updated_at = review_case.updated_at

            session.commit()

    def get_by_id(
        self,
        case_id: str,
    ) -> ReviewCase | None:
        with self._session_factory() as session:
            record = session.get(
                ReviewCaseRecord,
                case_id,
            )

            if record is None:
                return None

            return self._to_domain(record)

    def get_by_application_id(
        self,
        application_id: str,
    ) -> ReviewCase | None:
        with self._session_factory() as session:
            statement = select(ReviewCaseRecord).where(
                ReviewCaseRecord.application_id == application_id
            )

            record = session.scalar(statement)

            if record is None:
                return None

            return self._to_domain(record)

    @staticmethod
    def _to_record(
        review_case: ReviewCase,
    ) -> ReviewCaseRecord:
        return ReviewCaseRecord(
            case_id=review_case.case_id,
            application_id=review_case.application_id,
            status=review_case.status.value,
            created_at=review_case.created_at,
            updated_at=review_case.updated_at,
        )

    @staticmethod
    def _to_domain(
        record: ReviewCaseRecord,
    ) -> ReviewCase:
        review_case = ReviewCase(
            case_id=record.case_id,
            application_id=record.application_id,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )

        object.__setattr__(
            review_case,
            "status",
            CaseStatus(record.status),
        )

        return review_case