# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Two-service monorepo: a React SPA in `frontend/` and a Django REST API in `backend/`. They are independent processes with no shared build step or reverse proxy — the frontend talks to the backend directly over HTTP via axios.

## Commands

### Frontend (`frontend/`)

```
npm run dev       # start Vite dev server (http://localhost:5173)
npm run build     # production build
npm run preview   # preview the production build
npm run lint      # oxlint
```

No frontend test runner is configured yet.

### Backend (`backend/`)

Activate the virtualenv first — it is not auto-activated:

```
source venv/bin/activate
```

```
python manage.py runserver 8000     # dev server (http://localhost:8000)
python manage.py migrate            # apply migrations
python manage.py makemigrations     # create migrations after model changes
python manage.py test               # run full test suite
python manage.py test api.tests.test_health                              # one test module
python manage.py test api.tests.test_health.HealthCheckTests.test_health_check_returns_ok  # one test
```

## Architecture

**Frontend → backend wiring**: `frontend/src/api/client.js` is a preconfigured axios instance with `baseURL` set to `VITE_API_BASE_URL` (env var) or `http://localhost:8000/api` by default. All API calls should go through this client rather than calling axios directly, so the base URL stays centralized.

**Routing**: `BrowserRouter` wraps the app in `frontend/src/main.jsx`; routes are declared in `frontend/src/App.jsx`. Route-level components live in `frontend/src/pages/`.

**Styling**: Tailwind CSS v4 via the `@tailwindcss/vite` plugin (registered in `vite.config.js`). There is no `tailwind.config.js`/`postcss.config.js` — v4's Vite plugin doesn't need them for standard usage. Global styles are a single `@import "tailwindcss"` in `frontend/src/index.css`.

**Backend app structure**: The `api` Django app splits `views.py` and `tests.py` into packages (`api/views/`, `api/tests/`) instead of Django's default flat files, so each endpoint/test module gets its own file. Follow this pattern for new endpoints: add a view module under `api/views/`, re-export it from `api/views/__init__.py`, then register the route in `api/urls.py`. `api/models.py` and `api/admin.py` are still Django's untouched defaults (no models defined yet) — split those into packages too once they have real content, following the same convention.

**CORS**: `django-cors-headers` is configured with an explicit `CORS_ALLOWED_ORIGINS` allowlist in `config/settings.py` (currently just the Vite dev origins, `localhost:5173` / `127.0.0.1:5173`). Update this list if the frontend runs on a different origin.

**Database**: PostgreSQL, configured in `config/settings.py` via `os.environ`, loaded from `backend/.env` through `python-dotenv` (`load_dotenv` is called at the top of `settings.py`). Never hardcode DB credentials in `settings.py` — add new env vars to both `backend/.env` (actual values, gitignored) and `backend/.env.example` (template, committed).

**Django project layout**: `config/` is the Django project package (settings/urls/wsgi/asgi); `api/` is the (currently only) Django app, mounted at `/api/` in `config/urls.py`.
