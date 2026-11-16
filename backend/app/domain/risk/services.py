from typing import Protocol

from app.domain.application.models import CreditApplication
from app.domain.risk.models import RiskAssessment


class RiskService(Protocol):
    def assess(self, application: CreditApplication) -> RiskAssessment:
        ...