# Backend Design — Article Platform

**Stack:** FastAPI · MongoDB · Redis · REST API

---

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTPS/REST
┌──────▼──────────────────────────┐
│  FastAPI (Uvicorn + Gunicorn)   │
│  ┌────────────────────────────┐ │
│  │ /api/v1 routers            │ │
│  │ features/<feature>/...     │ │
│  │   router → service → repo  │ │
│  │ core/  (config, security)  │ │
│  │ shared/ (deps, pagination) │ │
│  └────────────────────────────┘ │
└──────┬──────────────┬───────────┘
       │              │
   ┌───▼────┐    ┌────▼────┐
   │MongoDB │    │  Redis  │  (cache, rate-limit, sessions)
   └────────┘    └─────────┘
```

## Project layout — feature-based modular

Vertical slices: each feature owns its router, schemas, models, service, repository, dependencies, and exceptions. Cross-cutting concerns live in `core/` (framework-agnostic primitives) and `shared/` (helpers that compose features).

```
app/
├── main.py                  # FastAPI app + lifespan; mounts feature routers
├── core/                    # framework-agnostic primitives
│   ├── config.py            # pydantic-settings
│   ├── security.py          # JWT encode/decode, argon2 hashing
│   ├── exceptions.py        # base AppError + global handler
│   └── logging.py
├── db/
│   ├── mongo.py             # Motor client (async)
│   └── indexes.py           # central index registry, run on startup
├── shared/                  # cross-feature helpers (no business logic)
│   ├── dependencies.py      # get_db, pagination params
│   └── pagination.py        # cursor codec
└── features/
    ├── auth/
    │   ├── router.py        # /auth routes
    │   ├── schemas.py       # LoginRequest, TokenPair, ...
    │   ├── models.py        # RefreshTokenDoc (Redis), session shapes
    │   ├── service.py       # AuthService: login, refresh, revoke
    │   ├── repository.py    # token store (Redis)
    │   ├── dependencies.py  # get_current_user, require_role
    │   └── exceptions.py    # InvalidCredentials, TokenRevoked, ...
    ├── users/               # same shape
    ├── articles/            # same shape
    ├── comments/            # same shape
    ├── tags/                # same shape
    └── media/               # same shape
```

**Layering inside a feature:** `router → service → repository`. Routers stay thin (parse, authorize, delegate). Services own business logic and orchestrate across repositories. Repositories own all Motor/Redis queries — no DB calls leak into services.

**Cross-feature dependencies:** import from the owning feature's public surface — typically `dependencies.py` (e.g. `from app.features.auth.dependencies import get_current_user`) or `service.py`. Avoid reaching into another feature's `repository.py` directly; go through its service.

**Why this layout:** adding a feature touches one directory. Removing a feature is a `rm -rf`. Tests for a feature live next to it (`features/articles/tests/`). The old layered split (`models/`, `services/`, `repositories/` as top-level dirs) forced edits across 5 directories per change and made ownership ambiguous.

## Data model (MongoDB collections)

### `users`
```jsonc
{
  _id: ObjectId,
  email: "...",            // unique
  username: "...",         // unique
  password_hash: "...",
  display_name, bio, avatar_url,
  role: "user" | "author" | "admin",
  created_at, updated_at
}
```

### `articles` — the hot collection
```jsonc
{
  _id: ObjectId,
  slug: "kebab-title-abc12", // unique
  title, subtitle,
  content: "...",            // markdown
  excerpt,
  cover_image,
  author_id: ObjectId,
  author_snapshot: { username, display_name, avatar_url }, // denormalized for list views
  tags: ["python", "fastapi"],
  status: "draft" | "published" | "archived",
  published_at, created_at, updated_at,
  stats: { views: 0, likes: 0, comments: 0 }, // counters
  reading_time_min: 7
}
```

### `comments` — flat with `parent_id` for threading
```jsonc
{ _id, article_id, author_id, parent_id?, body, created_at, edited_at? }
```

### `likes`
`{ user_id, article_id }` with compound unique index — prevents double-likes; counter in article is updated atomically.

### `tags`
`{ name, slug, article_count }` — maintained by background task.

### Why denormalize `author_snapshot`?
Article lists are read-heavy. Embedding cheap, immutable-ish author fields avoids a `$lookup` per item. Update via a background job when the author changes their profile.

## Indexes (critical for Mongo perf)

```python
articles: [
  ("slug", unique=True),
  ("status", "published_at" desc),
  ("author_id", "published_at" desc),
  ("tags", "published_at" desc),
  text index on (title, subtitle, content),    # for /search
]
users:    [("email", unique), ("username", unique)]
comments: [("article_id", "created_at"), ("parent_id",)]
likes:    [("user_id", "article_id"), unique]
```

## REST API surface (v1)

| Method | Path | Notes |
|---|---|---|
| POST | `/auth/register` | returns access + refresh JWT |
| POST | `/auth/login` | |
| POST | `/auth/refresh` | |
| GET | `/users/me` / `/users/{username}` | |
| PATCH | `/users/me` | |
| GET | `/articles` | filters: `tag`, `author`, `q`, `status`; cursor pagination |
| POST | `/articles` | author/admin only |
| GET | `/articles/{slug}` | increments view counter (async) |
| PATCH | `/articles/{slug}` | owner/admin |
| DELETE | `/articles/{slug}` | owner/admin |
| POST | `/articles/{slug}/like` / DELETE | idempotent |
| GET | `/articles/{slug}/comments` | |
| POST | `/articles/{slug}/comments` | |
| PATCH/DELETE | `/comments/{id}` | |
| GET | `/tags` / `/tags/{slug}` | |
| POST | `/media` | presigned S3 URL |

### Pagination
Use **cursor pagination** (`?cursor=<base64(published_at,_id)>&limit=20`), not offset — Mongo `skip` is O(n) and degrades on large lists.

### Auth
JWT access (~15 min) + refresh (~30 day, rotated). Refresh tokens stored hashed in Redis so they can be revoked. Argon2id for password hashing. `Depends(get_current_user)` for protected routes; `require_role("author")` for role gates.

## Cross-cutting concerns

- **Validation** — Pydantic v2 schemas, separate `ArticleCreate` / `ArticleUpdate` / `ArticleRead`.
- **Errors** — typed `AppError` hierarchy → uniform `{code, message, details}` JSON via exception handler.
- **Rate limiting** — Redis token bucket on auth + write endpoints.
- **Background work** — `BackgroundTasks` for cheap stuff (view counts), Celery/ARQ for heavier (search index, email, image processing).
- **Search** — Mongo text index is fine for v1; graduate to Meilisearch/OpenSearch if needed.
- **Observability** — structured JSON logs with request ID, Prometheus metrics, OpenTelemetry traces.
- **Tests** — `pytest-asyncio` + `httpx.AsyncClient` against an ephemeral Mongo (testcontainers); unit-test services with a fake repo.
- **Deploy** — Docker, env via `pydantic-settings`, healthcheck at `/healthz`, readiness probe checks Mongo + Redis.

## Key tradeoffs

1. **Denormalizing author into articles** speeds reads but adds a sync job — worth it for a read-heavy feed.
2. **Counters on the article doc** (likes/views) require atomic `$inc` and can drift slightly under contention; acceptable for social-style metrics, not for billing.
3. **Mongo text search** is a v1 shortcut — plan the Meilisearch escape hatch early (event-driven sync).
