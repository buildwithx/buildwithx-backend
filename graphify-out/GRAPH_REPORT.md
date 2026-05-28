# Graph Report - .  (2026-05-28)

## Corpus Check
- Corpus is ~4,282 words - fits in a single context window. You may not need a graph.

## Summary
- 248 nodes · 289 edges · 77 communities (60 shown, 17 thin omitted)
- Extraction: 65% EXTRACTED · 30% INFERRED · 5% AMBIGUOUS · INFERRED: 87 edges (avg confidence: 0.74)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]

## God Nodes (most connected - your core abstractions)
1. `AuthService` - 15 edges
2. `AuthRepository` - 12 edges
3. `get_current_user()` - 11 edges
4. `FakeRepository` - 10 edges
5. `Authentication Service` - 10 edges
6. `PyObjectId` - 9 edges
7. `get_auth_service()` - 8 edges
8. `Application Settings Configuration` - 8 edges
9. `Security Utilities (JWT & Password Hashing)` - 8 edges
10. `AppError` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Feature-based modular architecture` --conceptually_related_to--> `register()`  [INFERRED]
  README.md → features/auth/router.py
- `Router-Service-Repository layering pattern` --conceptually_for--> `register()`  [INFERRED]
  README.md → features/auth/router.py
- `Router-Service-Repository layering pattern` --conceptually_related_to--> `AuthService`  [INFERRED]
  README.md → app/features/auth/service.py
- `InvalidCredentials` --implements--> `Typed AppError exception hierarchy`  [INFERRED]
  app/features/auth/exceptions.py → README.md
- `UserAlreadyExists` --implements--> `Typed AppError exception hierarchy`  [INFERRED]
  app/features/auth/exceptions.py → README.md

## Hyperedges (group relationships)
- **Authentication Feature Components** — app_features_auth_service, app_features_auth_service_register, app_features_auth_service_login, app_features_auth_service_refresh, app_features_auth_service_logout [EXTRACTED 1.00]
- **Comments Feature Stub Files** — app_features_comments_service, app_features_comments_models, app_features_comments_schemas, app_features_comments_router, app_features_comments_repository, app_features_comments_dependencies, app_features_comments_exceptions [EXTRACTED 1.00]
- **Core Infrastructure Modules** — app_core_config, app_core_security, app_core_exceptions, app_core_logging, app_core_request_id [EXTRACTED 1.00]
- **JWT Token Lifecycle Operations** — app_features_auth_service_register, app_features_auth_service_login, app_features_auth_service_refresh, app_features_auth_service_logout [INFERRED 0.90]
- **Auth API endpoints** — auth_router_register, auth_router_login, auth_router_refresh, auth_router_me, auth_router_logout [EXTRACTED 1.00]
- **Auth request/response schemas** — auth_schemas_RegisterRequest, auth_schemas_LoginRequest, auth_schemas_RefreshRequest, auth_schemas_TokenPair, auth_schemas_UserRead, auth_schemas_LogoutRequest [EXTRACTED 1.00]
- **Auth domain exceptions** — auth_exceptions_InvalidCredentials, auth_exceptions_UserAlreadyExists, auth_exceptions_InvalidToken, auth_exceptions_ForbiddenError [EXTRACTED 1.00]
- **Auth dependency injection chain** — auth_dependencies_get_auth_service, auth_dependencies_get_current_user, auth_dependencies_require_role [EXTRACTED 1.00]
- **Database connection providers** — db_mongo_get_database, db_redis_get_redis [EXTRACTED 1.00]
- **Complete auth flow (register through logout)** — auth_router_register, auth_router_login, auth_router_refresh, auth_router_me, auth_router_logout, auth_service_AuthService, auth_repository_AuthRepository, auth_dependencies_get_current_user [INFERRED 0.85]
- **Auth test infrastructure** — tests_conftest, tests_conftest_FakeRepository, test_auth_register [EXTRACTED 1.00]
- **Core architectural patterns and rationale** — concept_router_service_repo_layering, concept_feature_modular_layout, concept_jwt_refresh_token_revocation, concept_author_snapshot_denormalization, concept_cursor_pagination, concept_apperror_hierarchy, concept_centralized_indexes [EXTRACTED 1.00]

## Communities (77 total, 17 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.12
Nodes (23): Articles Exceptions, get_current_user(), require_role(), ForbiddenError, InvalidCredentials, InvalidToken, UserAlreadyExists, UserDocument (+15 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (14): UserDocument, LoginRequest, LogoutRequest, RefreshRequest, RegisterRequest, UserRead, BaseHTTPMiddleware, BaseModel (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.17
Nodes (16): get_auth_service(), login(), logout(), me(), refresh(), register(), LoginRequest, LogoutRequest (+8 more)

### Community 3 - "Community 3"
Cohesion: 0.24
Nodes (10): TokenPair, AuthService, create_access_token(), create_refresh_token(), create_token(), decode_token(), hash_password(), TokenType (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.20
Nodes (7): AppError, ForbiddenError, InvalidCredentials, InvalidToken, UserAlreadyExists, AppError, Exception

### Community 5 - "Community 5"
Cohesion: 0.14
Nodes (16): Articles Dependencies, Articles Models, Articles Repository, Articles Router, Articles Schemas, Articles Service, Tags Dependencies, Tags Exceptions (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.22
Nodes (11): Application Settings Configuration, Application Error Handling, AppError Base Exception Class, Security Utilities (JWT & Password Hashing), Authentication Service, User Login Flow, User Logout Flow, Token Refresh Flow (+3 more)

### Community 8 - "Community 8"
Cohesion: 0.20
Nodes (4): JSONFormatter, Structured JSON logging with per-request context.  `setup_logging` installs a JS, Configure the root logger to emit JSON to stdout. Idempotent., setup_logging()

### Community 10 - "Community 10"
Cohesion: 0.52
Nodes (7): Media Feature Dependencies, Media Feature Exceptions, Media Feature Models, Media Feature Repository, Media Feature Router, Media Feature Schemas, Media Feature Service

### Community 11 - "Community 11"
Cohesion: 0.83
Nodes (4): Structured JSON Logging Module, JSON Log Formatter, Request ID Context Variable, Request ID Middleware

### Community 12 - "Community 12"
Cohesion: 0.67
Nodes (3): BaseSettings, get_settings(), Settings

### Community 14 - "Community 14"
Cohesion: 0.50
Nodes (4): Users Feature Dependencies, Users Feature Exceptions, Users Feature Repository, Users Feature Router

## Ambiguous Edges - Review These
- `Users Feature Exceptions` → `Users Feature Router`  [AMBIGUOUS]
  app/features/users/router.py · relation: references
- `Users Feature Router` → `Users Feature Dependencies`  [AMBIGUOUS]
  app/features/users/router.py · relation: references
- `Users Feature Router` → `Users Feature Repository`  [AMBIGUOUS]
  app/features/users/router.py · relation: references
- `Media Feature Service` → `Media Feature Repository`  [AMBIGUOUS]
  app/features/media/service.py · relation: references
- `Media Feature Service` → `Media Feature Models`  [AMBIGUOUS]
  app/features/media/service.py · relation: references
- `Media Feature Service` → `Media Feature Schemas`  [AMBIGUOUS]
  app/features/media/service.py · relation: references
- `Media Feature Service` → `Media Feature Exceptions`  [AMBIGUOUS]
  app/features/media/service.py · relation: references
- `Media Feature Service` → `Media Feature Router`  [AMBIGUOUS]
  app/features/media/router.py · relation: references
- `Media Feature Models` → `Media Feature Router`  [AMBIGUOUS]
  app/features/media/router.py · relation: references
- `Media Feature Models` → `Media Feature Repository`  [AMBIGUOUS]
  app/features/media/repository.py · relation: references
- `Media Feature Schemas` → `Media Feature Router`  [AMBIGUOUS]
  app/features/media/router.py · relation: references
- `Media Feature Exceptions` → `Media Feature Router`  [AMBIGUOUS]
  app/features/media/router.py · relation: references
- `Media Feature Router` → `Media Feature Dependencies`  [AMBIGUOUS]
  app/features/media/router.py · relation: references
- `Media Feature Router` → `Media Feature Repository`  [AMBIGUOUS]
  app/features/media/router.py · relation: references
- `Shared Pagination (Cursor Codec)` → `Shared Dependencies (get_db, pagination params)`  [AMBIGUOUS]
  app/shared/dependencies.py · relation: references

## Knowledge Gaps
- **34 isolated node(s):** `Articles Init`, `Articles Repository`, `Articles Dependencies`, `Tags Init`, `Tags Exceptions` (+29 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Users Feature Exceptions` and `Users Feature Router`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Users Feature Router` and `Users Feature Dependencies`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Users Feature Router` and `Users Feature Repository`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Media Feature Service` and `Media Feature Repository`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Media Feature Service` and `Media Feature Models`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Media Feature Service` and `Media Feature Schemas`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Media Feature Service` and `Media Feature Exceptions`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._