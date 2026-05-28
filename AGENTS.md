# AGENTS.md

## Project state

The auth feature is implemented (register, login, refresh, logout, me). Other features (users, articles, comments, tags, media) are stubs. CI/CD is set up with GitHub Actions.

## Commands

**Package manager:** `uv` (not pip)

```
uv sync                    # install all deps (including dev)
uv run uvicorn app.main:app --reload  # dev server
uv run ruff check .         # lint
uv run ruff format .        # format
uv run mypy app             # typecheck
uv run pyright app          # typecheck (alt)
uv run pytest               # run all tests
uv run pytest -k <name>     # run focused test
uv run pre-commit run --all-files  # run all hooks on all files
```

**Order:** `ruff format` → `ruff check` → `mypy` → `pytest`

**Pre-commit:** Hooks run automatically on commit (`ruff-format`, `ruff --fix`, `mypy app`). See `.pre-commit-config.yaml`.

**CI:** GitHub Actions (`.github/workflows/ci.yml`) runs format, lint, typecheck, and tests on push/PR to main.

## Architecture

**Feature-based modular layout** — vertical slices, not horizontal layers. Each feature under `app/features/<feature>/` owns: `router.py`, `schemas.py`, `models.py`, `service.py`, `repository.py`, `dependencies.py`, `exceptions.py`.

**Layering rule:** `router → service → repository`
- Routers: parse, authorize, delegate. No DB calls.
- Services: business logic. No DB calls.
- Repositories: all Motor/Redis queries live here only.

**Cross-feature imports:** go through `dependencies.py` or `service.py`. **Never import another feature's `repository.py`.** Auth (`get_current_user`, `require_role`) from `app.features.auth.dependencies` is the one exception others depend on.

**`core/` vs `shared/`:**
- `core/` — framework-agnostic (config, JWT, argon2, AppError, logging). Imports nothing from app.
- `shared/` — cross-feature helpers (get_db, pagination cursor). May import `core/`. No business logic.
- If adding business logic to `shared/`, it belongs in a feature instead.

## Architectural decisions (do not undo)

- **Cursor pagination** via `app/shared/pagination.py` — encodes `(published_at, _id)` as base64. Never use offset/skip.
- **`author_snapshot` denormalized** into article docs for read-heavy lists. Resync via background job when authors change profiles.
- **Counters** (`stats.views`, `stats.likes`, `stats.comments`) on article doc via atomic `$inc`. Acceptable drift under contention.
- **Refresh tokens hashed in Redis** (revocable). Access JWT ~15min, refresh ~30d, rotated on use. Argon2id for passwords.
- **Indexes** defined centrally in `app/db/indexes.py`, run on startup. Add new indexes there, not ad-hoc.
- **BackgroundTasks** for cheap work (view counts). Celery/ARQ for heavy (search index, email, images).
- **Errors**: typed `AppError` hierarchy → `{code, message, details}`. Extend in feature `exceptions.py`. **Never raise bare `HTTPException` from services.**
- **Pydantic v2** with separate `*Create` / `*Update` / `*Read` schemas.

## Testing

- `pytest-asyncio` + `httpx.AsyncClient`
- Tests co-located: `app/tests/`
- Use `FakeRepository` fixtures to unit-test services (no Docker required)
- Integration tests can use testcontainers for ephemeral Mongo/Redis when needed

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, invoke the `skill` tool with `skill: "graphify"` before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
