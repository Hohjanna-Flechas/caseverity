from app.infrastructure.database.session import SessionFactory
from app.infrastructure.persistence.postgres_applications import (
    PostgresApplicationRepository,
)
from app.infrastructure.persistence.postgres_review_cases import (
    PostgresReviewCaseRepository,
)


def get_application_repository() -> PostgresApplicationRepository:
    return PostgresApplicationRepository(
        session_factory=SessionFactory,
    )


def get_review_case_repository() -> PostgresReviewCaseRepository:
    return PostgresReviewCaseRepository(
        session_factory=SessionFactory,
    )