# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current state

This repo is at the **design-doc + scaffolding stage**. `README.md` describes the intended architecture, and `app/` contains the directory skeleton with empty `__init__.py` and stub module files, but no logic is implemented yet.

- All files under `app/` are empty (0 bytes / just `pass`-able stubs).
- No `requirements.txt`, `pyproject.toml`, or lockfile exists yet.
- `.env` and `.env.local` are empty.
- A `.venv/` (Python 3.14.3) is checked out but has no project dependencies installed.

When asked to implement something, **scaffold the missing dependency manifest as part of the work** (the README pins the stack: FastAPI, Motor, Redis, Pydantic v2, argon2, pytest-asyncio, httpx) — don't assume `pip install` of a non-existent requirements file will work.

## Architecture: feature-based modular

The project uses **vertical feature slices**, not horizontal layers. Each feature under `app/features/<feature>/` owns its full stack:

```
app/
├── main.py                  # FastAPI app + lifespan; mounts feature routers
├── core/                    # framework-agnostic primitives
│   ├── config.py            # pydantic-settings
│   ├── security.py          # JWT encode/decode, argon2
│   ├── exceptions.py        # base AppError + global handler
│   └── logging.py
├── db/
│   ├── mongo.py             # Motor client
│   └── indexes.py           # central index registry, run on startup
├── shared/                  # cross-feature helpers (no business logic)
│   ├── dependencies.py      # get_db, pagination params
│   └── pagination.py        # cursor codec
└── features/
    ├── auth/  users/  articles/  comments/  tags/  media/
    │   ├── router.py        # FastAPI routes for this feature
    │   ├── schemas.py       # request/response DTOs (Pydantic)
    │   ├── models.py        # Mongo document models (Pydantic)
    │   ├── service.py       # business logic
    │   ├── repository.py    # Motor queries — no DB calls outside this file
    │   ├── dependencies.py  # feature-local Depends (e.g. get_current_user)
    │   └── exceptions.py    # feature-local AppError subclasses
```

### Layering rule (inside each feature)

`router → service → repository`. Routers parse/authorize/delegate. Services own business logic. Repositories own Motor/Redis queries. **No DB calls in routers or services.** No business logic in routers or repositories.

### Cross-feature imports

Import from the owning feature's `dependencies.py` or `service.py` — those are the public surface. **Do not import another feature's `repository.py` directly.** Go through its service.

Concretely: other features get `get_current_user` and `require_role` from `app.features.auth.dependencies`. The auth feature is allowed to be a dependency of others; that's not a cycle.

### `core/` vs `shared/` vs `features/`

- `core/` — framework-agnostic primitives that have no concept of features (config, JWT codec, password hash, base `AppError`, logging). Imported by everything; imports nothing from the app.
- `shared/` — cross-feature helpers like the cursor pagination codec and `get_db`. May import from `core/`. Should not contain business logic.
- `features/` — everything else. A feature may import from `core/`, `shared/`, and other features' public surfaces.

If you find yourself adding business logic to `shared/`, it probably belongs in a feature.

## Architectural decisions worth preserving

These are choices the README makes deliberately. Don't undo them without a reason.

- **Cursor pagination**, not offset. Mongo `skip` is O(n) and degrades on large lists. Cursor encodes `(published_at, _id)` as base64. Codec lives in `app/shared/pagination.py` so every feature uses the same encoding.
- **`author_snapshot` denormalized into `articles`**. Article lists are read-heavy; this avoids a `$lookup` per item. A background job must resync when authors edit their profile — don't drop the snapshot without replacing the sync path.
- **Counters (`stats.views`, `stats.likes`, `stats.comments`) on the article doc** via atomic `$inc`. Accepted to drift slightly under contention; **do not** use this pattern for anything billing-related.
- **Refresh tokens hashed in Redis** so they can be revoked. Access JWT ~15min, refresh ~30d, rotated on use. Argon2id for passwords. Token storage lives in `features/auth/repository.py`.
- **Mongo text index for `/search`** is a v1 shortcut. The README explicitly plans a Meilisearch/OpenSearch escape hatch — keep search behind `ArticleService` so the backing store can be swapped event-driven without touching the router.
- **`BackgroundTasks` for cheap work** (view counts), **Celery/ARQ for heavy** (search index, email, images). Don't put heavy work in `BackgroundTasks`.
- **Indexes are defined in `app/db/indexes.py` and run on startup.** When adding a new query pattern in a feature's repository, add the index here — don't rely on ad-hoc `createIndex` calls and don't scatter index definitions across features.

## Conventions implied by the spec

- API is versioned under `/api/v1`. Each feature's router is mounted under that prefix in `app/main.py`.
- Errors use a typed `AppError` hierarchy serialized as `{code, message, details}` via a FastAPI exception handler registered in `core/exceptions.py`. Feature-specific errors (e.g. `ArticleNotFound`, `InvalidCredentials`) extend `AppError` in the feature's `exceptions.py`. **Do not raise bare `HTTPException` from services.**
- Pydantic v2, with separate `*Create` / `*Update` / `*Read` schemas per resource in the feature's `schemas.py`.
- Tests use `pytest-asyncio` + `httpx.AsyncClient` against an ephemeral Mongo via testcontainers; services are unit-tested against fake repositories. Co-locate tests with the feature (`app/features/articles/tests/`) rather than a global `tests/` tree.
- Healthcheck at `/healthz`; readiness probe must check Mongo + Redis.

## Commands

No build/test/lint commands are wired up yet. When the project gets a `pyproject.toml` or `requirements.txt`, update this section with the actual invocations rather than guessing.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
