from fastapi import FastAPI

from app.api.routes.applications import router as applications_router


app = FastAPI(
    title="CaseVerity API",
    version="0.1.0",
)

app.include_router(applications_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}