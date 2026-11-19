from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def build_application_payload() -> dict[str, object]:
    return {
        "application_id": "APP-0001",
        "applicant_id": "SYNTH-0001",
        "created_at": "2026-11-18T16:00:00Z",
        "requested_amount": 6000,
        "credit_duration_months": 24,
        "credit_purpose": "education",
        "age": 34,
        "employment_status": "employed",
        "employment_duration": "1_to_4_years",
        "existing_credit_count": 1,
        "savings_status": "moderate",
        "installment_commitments": "medium",
        "housing_status": "rent",
        "credit_history": "existing_credit_paid",
        "guarantor_status": "none",
    }


def test_submit_application_returns_risk_assessment() -> None:
    response = client.post(
        "/applications",
        json=build_application_payload(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["application_id"] == "APP-0001"
    assert body["risk_assessment"]["risk_score"] == 0.64
    assert body["risk_assessment"]["risk_level"] == "medium"
    assert body["risk_assessment"]["assessment_source"] == "mock"


def test_submit_application_rejects_invalid_requested_amount() -> None:
    payload = build_application_payload()
    payload["requested_amount"] = -500

    response = client.post(
        "/applications",
        json=payload,
    )

    assert response.status_code == 422

    body = response.json()

    assert body["detail"][0]["loc"] == ["body", "requested_amount"]

def test_submit_application_returns_conflict_for_duplicate() -> None:
    payload = build_application_payload()
    payload["application_id"] = "APP-DUPLICATE-001"

    first_response = client.post(
        "/applications",
        json=payload,
    )

    second_response = client.post(
        "/applications",
        json=payload,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "application APP-DUPLICATE-001 already exists"
    }
