"""Integration tests for the FastAPI-powered IoT API server."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from iot.app import create_app


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Provide a TestClient instance backed by the IoT FastAPI app."""

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


def test_healthcheck_returns_ok(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_message_endpoint_returns_greeting(client: TestClient) -> None:
    response = client.get("/api/message")
    assert response.status_code == 200
    assert "Hello" in response.json()["message"]
