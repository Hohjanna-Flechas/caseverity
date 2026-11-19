from dataclasses import dataclass

from app.application.repositories.applications import ApplicationRepository
from app.domain.application.models import CreditApplication
from app.domain.risk.models import RiskAssessment
from app.domain.risk.services import RiskService


class DuplicateApplicationError(Exception):
    pass


@dataclass(slots=True)
class SubmitApplicationResult:
    application: CreditApplication
    risk_assessment: RiskAssessment


class SubmitApplication:
    def __init__(
        self,
        risk_service: RiskService,
        application_repository: ApplicationRepository,
    ) -> None:
        self._risk_service = risk_service
        self._application_repository = application_repository

    def execute(
        self,
        application: CreditApplication,
    ) -> SubmitApplicationResult:
        existing_application = self._application_repository.get_by_id(
            application.application_id
        )

        if existing_application is not None:
            raise DuplicateApplicationError(
                f"application {application.application_id} already exists"
            )

        self._application_repository.save(application)

        risk_assessment = self._risk_service.assess(application)

        return SubmitApplicationResult(
            application=application,
            risk_assessment=risk_assessment,
        )