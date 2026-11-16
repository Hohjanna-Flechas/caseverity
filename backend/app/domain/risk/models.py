from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(slots=True)
class RiskAssessment:
    application_id: str
    risk_score: float
    risk_level: RiskLevel
    risk_factors: tuple[str, ...]
    assessment_source: str
    assessed_at: datetime

    def __post_init__(self) -> None:
        if not self.application_id.strip():
            raise ValueError("application_id cannot be empty")

        if not 0 <= self.risk_score <= 1:
            raise ValueError("risk_score must be between 0 and 1")

        if not self.assessment_source.strip():
            raise ValueError("assessment_source cannot be empty")