from typing import Protocol

from app.domain.application.models import CreditApplication


class ApplicationRepository(Protocol):
    def save(self, application: CreditApplication) -> None:
        ...

    def get_by_id(
        self,
        application_id: str,
    ) -> CreditApplication | None:
        ...