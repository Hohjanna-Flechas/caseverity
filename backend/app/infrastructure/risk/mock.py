from datetime import datetime, timezone

from app.domain.application.models import CreditApplication
from app.domain.risk.models import RiskAssessment, RiskLevel


class MockRiskService:
    def assess(self, application: CreditApplication) -> RiskAssessment:
        return RiskAssessment(
            application_id=application.application_id,
            risk_score=0.64,
            risk_level=RiskLevel.MEDIUM,
            risk_factors=(
                "recent_credit_history",
                "existing_credit_commitments",
            ),
            assessment_source="mock",
            assessed_at=datetime.now(timezone.utc),
        )