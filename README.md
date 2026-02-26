# Home Energy Advisor

## Overview

This project is a full‑stack web application that allows users to
create a home profile and receive AI‑generated energy efficiency
recommendations.

The goal is to demonstrate: - Clean API design - Pragmatic
architecture - LLM integration - Developer‑friendly codebase

------------------------------------------------------------------------

**Deliverables:** This repo includes setup instructions, assumptions/tradeoffs, and an [AI Tool Usage Log](#ai-tool-usage-log) section below.

---

## Setup

**Prerequisites:** Python 3.9+ and Node.js 18+

No Docker or PostgreSQL required. SQLite is used by default.

**Tradeoffs:** I chose SQLite and a Docker-free setup so anyone can clone and run locally in minutes, without installing Docker or PostgreSQL. This keeps the task simple and quick to evaluate. SQLite is fine for low concurrency and single-user dev; for production or high-traffic use, we can switch to PostgreSQL via `DATABASE_URL` and `psycopg2-binary`. Docker can be re-added later for consistent deployment if needed.

### Quick start

```bash
# Clone and enter
git clone <repo-url>
cd home-energy-advisor

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

In a second terminal:

```bash
cd home-energy-advisor/frontend
npm run build
npm install
npm run dev
```

If TypeScript complains about missing Node types during build, install them once:

```bash
cd frontend
npm install --save-dev @types/node
```

### set the debug in .evn to true to see the swagger
#DEBUG=true

Open **http://localhost:3000** (backend runs on port 8000).

### Optional

- **.env:** Copy `example.env` to `backend/.env` to set `OPENAI_API_KEY` (or leave unset for mock recommendations).

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /api/homes | Create home (`size_sqm`, `year_built`, `heating_type`, `insulation`, `notes`) |
| GET    | /api/homes/{id} | Get home by id |
| POST   | /api/homes/{id}/advice | Get prioritized LLM recommendations |

**Body:** `heating_type`: `GAS` \| `OIL` \| `ELECTRIC` \| `HEAT_PUMP` \| `DISTRICT`. `insulation` (optional): `NONE` \| `PARTIAL` \| `GOOD` \| `EXCELLENT`.

---

## Tests

```bash
cd backend && pytest tests/ -v
```

---

## Assumptions and tradeoffs

- **LLM:** Recommendations are generated via OpenAI by default. If `OPENAI_API_KEY` is unset or the client is unavailable, the app can be configured to return mock recommendations so the flow is testable without API keys.
- **Scope:** Single home profile per submission; no user accounts or persistence of “sessions” beyond the created home record and its advice response.
- **Validation:** Living area and year built are validated on the backend; heating type is required. Frontend mirrors these rules for inline UX; backend remains the source of truth.
- **UI:** Frontend is a single-page flow (form → submit → show recommendations) with no routing. Designed for clarity and accessibility (e.g. min touch targets, ARIA where relevant).
- **Database:** SQLite by default for zero-setup local runs. Optional PostgreSQL: set `DATABASE_URL` and install `psycopg2-binary`. Migrations via Alembic.

- **The LLM integration** is intentionally synchronous: for this small, low‑traffic API FastAPI’s threadpool is sufficient, and going async would add complexity without a measurable benefit. If this grow into a high‑throughput service, the client and endpoints could be switched to async behind the same public API
---

## AI Tool Usage Log

I used AI coding assistants during development. Below is a concise log of tools, prompts, and outcomes.

### Which tools were used

- **ChatGPT** for code generation, refactors, and README updates.

### 2–3 prompts that worked well

1. **“Make the UI user friendly and redesign it as it looks ugly now.”**  
   Used to drive a full pass on the Vue frontend: design tokens, typography (Inter), card layout, form grid, button/input styling, and a simple fade-in for the recommendations block. The model proposed a teal primary palette and Apple-inspired spacing/shadows that I kept.

2. **“Your energy-saving recommendations card is not in the same position as the Your home details card.”**  
   Used to fix layout: the recommendations section was inside a full-width wrapper while the form card had `max-w-xl`, so they didn’t align. Prompt led to constraining the recommendations wrapper to `max-w-xl` so both cards share the same width and centering.

3. **“Add inline validation (clear error on edit, validate on blur)”**  
   Used to implement form validation in the Vue app: validate on blur, clear per-field errors when the user edits the field, and keep a single source of validation rules used by both blur and submit.

### What I used AI for vs. wrote myself

- **With AI:** Initial FastAPI structure, Pydantic schemas, Vue components (HomeForm, AdviceResults, UI primitives), Tailwind/CSS design tokens, Alembic migration style, and README structure.
- **By Me:** Product and API design (homes + advice endpoints), choice of stack (FastAPI, Vue, SQLite/Postgres), validation rules and enums, manual testing and fixes.

### One thing AI got wrong that I had to fix

- **Frontend (critical):** The generated form had no proper validation flow and showed errors only via `alert()`. Recommendations from the API were initially rendered in a way that could interpret HTML, creating an XSS risk if the LLM or data ever returned unsanitized content. I had to introduce structured inline validation (blur + submit), clear per-field errors, toast-based feedback, and ensure all API-sourced text is rendered as plain text (no `v-html` or unescaped output) so the app is both usable and safe.

- **Backend (critical):** The generated API did not enforce strict request validation on all inputs and returned raw Python tracebacks to the client on 500 errors, exposing internal paths and dependencies. I had to add strict Pydantic schemas for every endpoint, implement global exception handlers, and ensure only safe, structured error messages (e.g. `{"detail": "..."}`) are returned so production never leaks internals.

- Used Python 3.10 union types which caused runtime error on Python 3.9
- Fixed by switching to Optional typing

---
### Code tour (for new developers)

**Backend:** Request flow is `api/homes.py` → `services/` → `models/`. Schemas in `schemas/` define request/response shapes. Config lives in `core/config.py` (env vars, CORS); `core/database.py` sets up SQLAlchemy. Start at `main.py` and follow the router imports.

**Frontend:** `App.vue` orchestrates the form and results. `HomeForm.vue` handles input and validation; `AdviceResults.vue` renders recommendations. API calls are in `lib/api/homes.ts`.


## Project structure

- **backend/** – FastAPI app (`app/`, `alembic/`, `tests/`)
- **frontend/** – Vue 3 + TypeScript + Vite + Tailwind


## Project Directory Tree

```text
home-energy-advisor/
│
├─ backend/                        # FastAPI backend
│  │
│  ├─ app/                         # Application source code
│  │  │
│  │  ├─ api/                      # API route handlers
│  │  │   └─ homes.py
│  │  │
│  │  ├─ core/                     # Core infrastructure
│  │  │   ├─ config.py
│  │  │   ├─ database.py
│  │  │   └─ messages.py
│  │  │
│  │  ├─ models/                   # SQLAlchemy models
│  │  │   ├─ __init__.py
│  │  │   └─ home.py
│  │  │
│  │  ├─ schemas/                  # Pydantic schemas
│  │  │   ├─ __init__.py
│  │  │   ├─ home.py
│  │  │   └─ advice.py
│  │  │
│  │  ├─ services/                 # Business logic
│  │  │   ├─ __init__.py
│  │  │   ├─ home_service.py
│  │  │   └─ llm_service.py
│  │  │
│  │  └─ main.py                   # FastAPI entrypoint
│  │
│  ├─ alembic/                     # Database migrations
│  │  ├─ env.py
│  │  ├─ script.py.mako
│  │  └─ versions/
│  │      └─ 2026_02_23_12_00_abc123_initial_homes_table.py
│  │
│  ├─ tests/                       # Backend tests
│  │  ├─ conftest.py
│  │  ├─ test_api.py
│  │  └─ test_llm_service.py
│  │
│  ├─ alembic.ini
│  └─ requirements.txt
│
├─ frontend/                       # Vue + Typescript + Vite frontend
│  │
│  ├─ src/
│  │  │
│  │  ├─ components/
│  │  │  ├─ AdviceResults.vue
│  │  │  ├─ HomeForm.vue
│  │  │  ├─ ToastContainer.vue
│  │  │  └─ ui/
│  │  │     ├─ Button.vue
│  │  │     ├─ Card.vue
│  │  │     ├─ Input.vue
│  │  │     └─ Label.vue
│  │  │
│  │  ├─ composables/
│  │  │  └─ useToast.ts
│  │  │
│  │  ├─ lib/
│  │  │  ├─ utils.ts
│  │  │  └─ api/
│  │  │     ├─ client.ts
│  │  │     └─ homes.ts
│  │  │
│  │  ├─ types/
│  │  │  └─ home.ts
│  │  │
│  │  ├─ assets/
│  │  │  └─ main.css
│  │  │
│  │  ├─ App.vue
│  │  ├─ main.ts
│  │  └─ vite-env.d.ts
│  │
│  ├─ index.html
│  ├─ package.json
│  ├─ package-lock.json
│  ├─ tsconfig.json
│  └─ vite.config.ts
│
├─ README.md
├─ example.env
└─ .gitignore
```