"""Integration tests for the lightweight IoT API server."""

from __future__ import annotations

import json
from contextlib import closing
from http.client import HTTPConnection
from threading import Thread
from time import sleep

import pytest

from iot.app import create_server


@pytest.fixture
def running_server():
    """Start the IoT API server in a background thread for testing."""

    server = create_server(host="127.0.0.1", port=0)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    # Wait briefly to ensure the server is accepting connections
    sleep(0.1)
    yield server
    server.shutdown()
    thread.join()


def _request_json(server, path: str) -> tuple[int, dict[str, str]]:
    host, port = server.server_address
    with closing(HTTPConnection(host, port)) as connection:
        connection.request("GET", path)
        response = connection.getresponse()
        data = json.loads(response.read().decode("utf-8"))
    return response.status, data


def test_healthcheck_returns_ok(running_server) -> None:
    status, payload = _request_json(running_server, "/api/health")
    assert status == 200
    assert payload == {"status": "ok"}


def test_message_endpoint_returns_greeting(running_server) -> None:
    status, payload = _request_json(running_server, "/api/message")
    assert status == 200
    assert "Hello" in payload["message"]
