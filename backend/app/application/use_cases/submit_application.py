from dataclasses import dataclass

from app.domain.application.models import CreditApplication
from app.domain.risk.models import RiskAssessment
from app.domain.risk.services import RiskService


@dataclass(slots=True)
class SubmitApplicationResult:
    application: CreditApplication
    risk_assessment: RiskAssessment


class SubmitApplication:
    def __init__(self, risk_service: RiskService) -> None:
        self._risk_service = risk_service

    def execute(
        self,
        application: CreditApplication,
    ) -> SubmitApplicationResult:
        risk_assessment = self._risk_service.assess(application)

        return SubmitApplicationResult(
            application=application,
            risk_assessment=risk_assessment,
        )