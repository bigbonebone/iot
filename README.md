# IoT Web Platform

This repository contains a lightweight Python HTTP backend and a Vue 3
single-page application that together form the foundation of the IoT web
platform.

## Project structure

```
.
├── frontend/         # Vue 3 application powered by Vite
├── src/iot/          # Minimal Python HTTP backend package
└── tests/            # Pytest suite for backend components
```

## Backend setup

1. Create a virtual environment and install the backend in editable mode with
   development dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .[dev]
   ```
2. Launch the development server:
   ```bash
   python -m iot.app
   ```
3. The API exposes JSON endpoints such as `http://127.0.0.1:8000/api/message`
   that can be consumed by the Vue frontend.

## Frontend setup

1. Install Node.js 18+ and pnpm/npm/yarn.
2. Install dependencies and start the development server from the `frontend`
   directory:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Configure the Vite proxy (configured in `vite.config.js`) to forward `/api`
   requests to the Python server so both services work together seamlessly.

## Testing

Run the backend test suite with:
```bash
pytest
```
