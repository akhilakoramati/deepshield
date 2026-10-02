# DeepShield Phase 1

DeepShield is a React, FastAPI, and PostgreSQL platform for image, audio, and video authenticity verification. Phase 1 uses isolated mock detectors; production image, audio, and video models can replace those services without changing the API or frontend.

## Run locally

Start the existing PostgreSQL service without recreating its data:

```powershell
docker compose up -d db
```

Run the backend:

```powershell
cd backend
..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Run the React frontend in a second terminal:

```powershell
npm install
npx vite --host 127.0.0.1
```

Open http://127.0.0.1:5173. API documentation is available at http://127.0.0.1:8000/docs.

## Architecture

- `src/pages`: landing, auth, dashboard, upload, analysis, history, reports, and settings views.
- `src/services/api.js`: centralized Axios client with JWT injection and normalized errors.
- `src/context` and `src/hooks`: authenticated session state and protected routing.
- `backend/app/core`: environment configuration, security, and validation errors.
- `backend/app/models` and `backend/app/schemas`: database entities and API contracts.
- `backend/app/services`: business logic and isolated AI detector registry.
- `backend/app/routers`: HTTP endpoints only.

## API

Authentication:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/change-password`

Media and analysis:

- `POST /api/media/upload`
- `GET /api/media/{media_id}`
- `POST /api/analysis`
- `GET /api/analysis/{analysis_id}`
- `GET /api/analysis/history`
- `DELETE /api/analysis/{analysis_id}`
- `GET /api/dashboard/stats`

Reports:

- `GET /api/reports`
- `POST /api/reports`
- `GET /api/reports/{report_id}`

All protected endpoints use `Authorization: Bearer <jwt>`.

## Mock detector boundary

The registry at `backend/app/services/ai/registry.py` selects one detector by media type:

- `image_detector.py`: future EfficientNet integration point.
- `audio_detector.py`: future CNN + LSTM integration point.
- `video_detector.py`: future XceptionNet + LSTM integration point.

Each currently returns a deterministic Phase 1 mock result with `REAL`/`FAKE`, confidence, status, and summary.

## Configuration and security

Copy `.env.example` to `.env` and set a strong `JWT_SECRET` for non-local use. `DATABASE_URL` preserves the existing PostgreSQL connection. Passwords use salted scrypt hashes, uploaded files are limited to 50 MB, extensions and MIME categories are validated, and stored filenames are generated server-side.

The backend can also be built independently with `backend/Dockerfile`; the current `docker-compose.yml` PostgreSQL service and its named volume are intentionally preserved.

## PostgreSQL backup and restore

The Compose PostgreSQL service uses the named volume `deepshield_pgdata`. Create a logical backup from the project root with:

```powershell
docker compose exec -T db pg_dump -U $env:POSTGRES_USER -d $env:POSTGRES_DB -Fc > deepshield-$(Get-Date -Format yyyyMMdd-HHmm).dump
```

Restore a dump into the running database with:

```powershell
Get-Content .\deepshield-backup.dump -Encoding Byte | docker compose exec -T db pg_restore -U $env:POSTGRES_USER -d $env:POSTGRES_DB --clean --if-exists
```

Set `POSTGRES_USER` and `POSTGRES_DB` in the shell or `.env` before running these commands. Keep backup files outside source control and test restores before production incidents.
