from sqlalchemy.orm import Session, sessionmaker

from app.domain.application.models import CreditApplication
from app.infrastructure.database.models.applications import (
    CreditApplicationRecord,
)


class PostgresApplicationRepository:
    def __init__(
        self,
        session_factory: sessionmaker[Session],
    ) -> None:
        self._session_factory = session_factory

    def save(
        self,
        application: CreditApplication,
    ) -> None:
        record = self._to_record(application)

        with self._session_factory() as session:
            session.add(record)
            session.commit()

    def get_by_id(
        self,
        application_id: str,
    ) -> CreditApplication | None:
        with self._session_factory() as session:
            record = session.get(
                CreditApplicationRecord,
                application_id,
            )

            if record is None:
                return None

            return self._to_domain(record)

    @staticmethod
    def _to_record(
        application: CreditApplication,
    ) -> CreditApplicationRecord:
        return CreditApplicationRecord(
            application_id=application.application_id,
            applicant_id=application.applicant_id,
            created_at=application.created_at,
            requested_amount=application.requested_amount,
            credit_duration_months=application.credit_duration_months,
            credit_purpose=application.credit_purpose,
            age=application.age,
            employment_status=application.employment_status,
            employment_duration=application.employment_duration,
            existing_credit_count=application.existing_credit_count,
            savings_status=application.savings_status,
            installment_commitments=application.installment_commitments,
            housing_status=application.housing_status,
            credit_history=application.credit_history,
            guarantor_status=application.guarantor_status,
        )

    @staticmethod
    def _to_domain(
        record: CreditApplicationRecord,
    ) -> CreditApplication:
        return CreditApplication(
            application_id=record.application_id,
            applicant_id=record.applicant_id,
            created_at=record.created_at,
            requested_amount=record.requested_amount,
            credit_duration_months=record.credit_duration_months,
            credit_purpose=record.credit_purpose,
            age=record.age,
            employment_status=record.employment_status,
            employment_duration=record.employment_duration,
            existing_credit_count=record.existing_credit_count,
            savings_status=record.savings_status,
            installment_commitments=record.installment_commitments,
            housing_status=record.housing_status,
            credit_history=record.credit_history,
            guarantor_status=record.guarantor_status,
        )