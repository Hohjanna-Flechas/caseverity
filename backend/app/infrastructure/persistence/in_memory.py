from app.domain.application.models import CreditApplication


class InMemoryApplicationRepository:
    def __init__(self) -> None:
        self._applications: dict[str, CreditApplication] = {}

    def save(self, application: CreditApplication) -> None:
        self._applications[application.application_id] = application

    def get_by_id(
        self,
        application_id: str,
    ) -> CreditApplication | None:
        return self._applications.get(application_id)