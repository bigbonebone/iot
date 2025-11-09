"""IoT API implemented with the FastAPI web framework."""

from __future__ import annotations

import logging
from typing import Dict

import uvicorn
from fastapi import FastAPI

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Construct and configure the FastAPI application instance."""

    app = FastAPI(title="IoT API", version="0.1.0")

    @app.get("/api/health")
    def healthcheck() -> Dict[str, str]:
        """Return a simple health status payload."""

        return {"status": "ok"}

    @app.get("/api/message")
    def demo_message() -> Dict[str, str]:
        """Return a welcome message for the Vue frontend."""

        return {"message": "Hello from the Python backend!"}

    return app


app = create_app()


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Run the FastAPI application using Uvicorn."""

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logger.info("Starting IoT API server on %s:%s", host, port)
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    run()
