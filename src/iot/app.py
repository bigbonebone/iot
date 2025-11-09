"""Lightweight HTTP server exposing IoT API endpoints."""

from __future__ import annotations

import json
import logging
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable, Dict, Tuple

logger = logging.getLogger(__name__)

RouteKey = Tuple[str, str]
Handler = Callable[[], Dict[str, str]]


class IoTRequestHandler(BaseHTTPRequestHandler):
    """Request handler that dispatches to registered route callbacks."""

    routes: Dict[RouteKey, Handler] = {}
    server_version = "IoTServer/0.1"
    sys_version = ""

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        """Log HTTP requests using the standard logging module."""
        logger.info("%s - - [%s] " + format, self.address_string(), self.log_date_time_string(), *args)

    def do_GET(self) -> None:  # noqa: N802 (method name required by BaseHTTPRequestHandler)
        handler = self.routes.get(("GET", self.path))
        if handler is None:
            self.send_error(HTTPStatus.NOT_FOUND, "Endpoint not found")
            return
        payload = handler()
        self._send_json(payload)

    def _send_json(self, payload: Dict[str, str]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def route(method: str, path: str) -> Callable[[Handler], Handler]:
    """Register a handler for the given HTTP method and path."""

    method_upper = method.upper()

    def decorator(func: Handler) -> Handler:
        IoTRequestHandler.routes[(method_upper, path)] = func
        return func

    return decorator


@route("GET", "/api/health")
def healthcheck() -> Dict[str, str]:
    """Return a simple health status payload."""
    return {"status": "ok"}


@route("GET", "/api/message")
def demo_message() -> Dict[str, str]:
    """Return a welcome message for the Vue frontend."""
    return {"message": "Hello from the Python backend!"}


def create_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    """Create an HTTP server instance bound to the provided host and port."""

    return ThreadingHTTPServer((host, port), IoTRequestHandler)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Run the API server until interrupted."""

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    server = create_server(host, port)
    logger.info("Starting IoT API server on %s:%s", host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down IoT API server")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
