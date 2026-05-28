# Graph Report - /Users/chenter-jaksmok/Projects/buildwithx/buildwithx-backend  (2026-05-28)

## Corpus Check
- Corpus is ~4,438 words - fits in a single context window. You may not need a graph.

## Summary
- 267 nodes · 296 edges · 84 communities (65 shown, 19 thin omitted)
- Extraction: 65% EXTRACTED · 30% INFERRED · 5% AMBIGUOUS · INFERRED: 88 edges (avg confidence: 0.74)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Auth Schemas|Auth Schemas]]
- [[_COMMUNITY_Auth Service Layer|Auth Service Layer]]
- [[_COMMUNITY_AuthService Implementation|AuthService Implementation]]
- [[_COMMUNITY_Articles Feature|Articles Feature]]
- [[_COMMUNITY_Auth Dependencies & Exceptions|Auth Dependencies & Exceptions]]
- [[_COMMUNITY_AppError Hierarchy|AppError Hierarchy]]
- [[_COMMUNITY_App Core & Lifespan|App Core & Lifespan]]
- [[_COMMUNITY_Test Infrastructure|Test Infrastructure]]
- [[_COMMUNITY_Logging Module|Logging Module]]
- [[_COMMUNITY_Auth Repository Interface|Auth Repository Interface]]
- [[_COMMUNITY_Media Feature|Media Feature]]
- [[_COMMUNITY_Token Lifecycle|Token Lifecycle]]
- [[_COMMUNITY_Request ID & Logging|Request ID & Logging]]
- [[_COMMUNITY_Settings Configuration|Settings Configuration]]
- [[_COMMUNITY_Exception Handlers|Exception Handlers]]
- [[_COMMUNITY_Database Initialization|Database Initialization]]
- [[_COMMUNITY_Rate Limiting|Rate Limiting]]
- [[_COMMUNITY_Users Feature|Users Feature]]
- [[_COMMUNITY_Username Generation|Username Generation]]
- [[_COMMUNITY_Shared Helpers|Shared Helpers]]
- [[_COMMUNITY_Comments Service Stub|Comments Service Stub]]
- [[_COMMUNITY_Comments Models Stub|Comments Models Stub]]
- [[_COMMUNITY_Comments Schemas Stub|Comments Schemas Stub]]
- [[_COMMUNITY_Comments Exceptions Stub|Comments Exceptions Stub]]
- [[_COMMUNITY_Comments Router Stub|Comments Router Stub]]
- [[_COMMUNITY_Comments Repository Stub|Comments Repository Stub]]
- [[_COMMUNITY_Comments Dependencies Stub|Comments Dependencies Stub]]
- [[_COMMUNITY_Articles Init Module|Articles Init Module]]
- [[_COMMUNITY_Tags Init Module|Tags Init Module]]
- [[_COMMUNITY_Users Init Module|Users Init Module]]
- [[_COMMUNITY_Media Init Module|Media Init Module]]
- [[_COMMUNITY_Shared Init Module|Shared Init Module]]
- [[_COMMUNITY_DB Init Module|DB Init Module]]
- [[_COMMUNITY_Auth Router Include|Auth Router Include]]
- [[_COMMUNITY_Login Flow|Login Flow]]
- [[_COMMUNITY_ObjectId Validator|ObjectId Validator]]

## God Nodes (most connected - your core abstractions)
1. `AuthService` - 17 edges
2. `AuthRepository` - 13 edges
3. `get_current_user()` - 11 edges
4. `FakeRepository` - 11 edges
5. `PyObjectId` - 9 edges
6. `get_auth_service()` - 8 edges
7. `AuthService business logic class` - 8 edges
8. `AuthRepository data access class` - 8 edges
9. `AppError` - 7 edges
10. `TokenPair` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Feature-based modular architecture` --conceptually_related_to--> `register()`  [INFERRED]
  README.md → features/auth/router.py
- `create_indexes()` --implements--> `Centralized MongoDB index definitions`  [INFERRED]
  db/indexes.py → README.md
- `InvalidCredentials` --implements--> `Typed AppError exception hierarchy`  [INFERRED]
  app/features/auth/exceptions.py → README.md
- `UserAlreadyExists` --implements--> `Typed AppError exception hierarchy`  [INFERRED]
  app/features/auth/exceptions.py → README.md
- `InvalidToken` --implements--> `Typed AppError exception hierarchy`  [INFERRED]
  app/features/auth/exceptions.py → README.md

## Hyperedges (group relationships)
- **Core Infrastructure Modules** — app_core_config, app_core_security, app_core_exceptions, app_core_logging, app_core_request_id [EXTRACTED 1.00]
- **Comments Feature Stub Files** — app_features_comments_service, app_features_comments_models, app_features_comments_schemas, app_features_comments_router, app_features_comments_repository, app_features_comments_dependencies, app_features_comments_exceptions [EXTRACTED 1.00]
- **Auth request/response schemas** — auth_schemas_RegisterRequest, auth_schemas_LoginRequest, auth_schemas_RefreshRequest, auth_schemas_TokenPair, auth_schemas_UserRead, auth_schemas_LogoutRequest [EXTRACTED 1.00]
- **Auth domain exceptions** — auth_exceptions_InvalidCredentials, auth_exceptions_UserAlreadyExists, auth_exceptions_InvalidToken, auth_exceptions_ForbiddenError [EXTRACTED 1.00]
- **Auth API endpoints** — auth_router_register, auth_router_login, auth_router_refresh, auth_router_me, auth_router_logout [EXTRACTED 1.00]
- **Complete auth flow (register through logout)** — auth_router_register, auth_router_login, auth_router_refresh, auth_router_me, auth_router_logout, auth_service_AuthService, auth_repository_AuthRepository, auth_dependencies_get_current_user [INFERRED 0.85]
- **Auth dependency injection chain** — auth_dependencies_get_auth_service, auth_dependencies_get_current_user, auth_dependencies_require_role [EXTRACTED 1.00]
- **Core architectural patterns and rationale** — concept_router_service_repo_layering, concept_feature_modular_layout, concept_jwt_refresh_token_revocation, concept_author_snapshot_denormalization, concept_cursor_pagination, concept_apperror_hierarchy, concept_centralized_indexes [EXTRACTED 1.00]
- **Refresh token lifecycle (store-validate-revoke)** — auth_repository_token_storage, auth_repository_token_validation, auth_repository_token_revocation [EXTRACTED 0.95]
- **Authentication flows (register-login-refresh-logout)** — auth_service_register, auth_service_login, auth_service_refresh, auth_service_logout [EXTRACTED 0.90]
- **Error handling registration chain** — exceptions_AppError, exceptions_app_error_handler, exceptions_register_exception_handlers, main_register_exception_handlers [EXTRACTED 0.95]
- **Test fixture infrastructure** — conftest_FakeRepository, conftest_api_client [EXTRACTED 1.00]
- **Database initialization and indexing** — mongo_database, mongo_get_database, indexes_create_indexes, main_lifespan [EXTRACTED 0.90]
- **Auth API endpoints** — auth_router_register, auth_router_login, auth_router_refresh, auth_router_me, auth_router_logout [EXTRACTED 1.00]
- **Auth request/response schemas** — auth_schemas_RegisterRequest, auth_schemas_LoginRequest, auth_schemas_RefreshRequest, auth_schemas_TokenPair, auth_schemas_UserRead, auth_schemas_LogoutRequest [EXTRACTED 1.00]
- **Auth domain exceptions** — auth_exceptions_InvalidCredentials, auth_exceptions_UserAlreadyExists, auth_exceptions_InvalidToken, auth_exceptions_ForbiddenError [EXTRACTED 1.00]
- **Auth dependency injection chain** — auth_dependencies_get_auth_service, auth_dependencies_get_current_user, auth_dependencies_require_role [EXTRACTED 1.00]
- **Database connection providers** — db_mongo_get_database, db_redis_get_redis [EXTRACTED 1.00]
- **Complete auth flow (register through logout)** — auth_router_register, auth_router_login, auth_router_refresh, auth_router_me, auth_router_logout, auth_service_AuthService, auth_repository_AuthRepository, auth_dependencies_get_current_user [INFERRED 0.85]
- **Auth test infrastructure** — tests_conftest, tests_conftest_FakeRepository, test_auth_register [EXTRACTED 1.00]
- **Core architectural patterns and rationale** — concept_router_service_repo_layering, concept_feature_modular_layout, concept_jwt_refresh_token_revocation, concept_author_snapshot_denormalization, concept_cursor_pagination, concept_apperror_hierarchy, concept_centralized_indexes [EXTRACTED 1.00]

## Communities (84 total, 19 thin omitted)

### Community 0 - "Auth Schemas"
Cohesion: 0.12
Nodes (15): UserDocument, LoginRequest, LogoutRequest, RefreshRequest, RegisterRequest, TokenPair, UserRead, BaseHTTPMiddleware (+7 more)

### Community 1 - "Auth Service Layer"
Cohesion: 0.14
Nodes (20): get_auth_service(), AuthRepository data access class, login(), logout(), refresh(), register(), LoginRequest, LogoutRequest (+12 more)

### Community 2 - "AuthService Implementation"
Cohesion: 0.19
Nodes (9): AuthService, create_access_token(), create_refresh_token(), create_token(), decode_token(), hash_password(), TokenType, verify_password() (+1 more)

### Community 3 - "Articles Feature"
Cohesion: 0.14
Nodes (16): Articles Dependencies, Articles Models, Articles Repository, Articles Router, Articles Schemas, Articles Service, Tags Dependencies, Tags Exceptions (+8 more)

### Community 4 - "Auth Dependencies & Exceptions"
Cohesion: 0.19
Nodes (15): Articles Exceptions, get_current_user(), require_role(), ForbiddenError, InvalidCredentials, InvalidToken, UserAlreadyExists, CLAUDE.md project guidance (+7 more)

### Community 5 - "AppError Hierarchy"
Cohesion: 0.20
Nodes (7): AppError, ForbiddenError, InvalidCredentials, InvalidToken, UserAlreadyExists, AppError, Exception

### Community 6 - "App Core & Lifespan"
Cohesion: 0.15
Nodes (9): Application Settings Configuration, Security Utilities (JWT & Password Hashing), lifespan(), UserDocument, me(), UserRead, create_indexes(), get_database() (+1 more)

### Community 7 - "Test Infrastructure"
Cohesion: 0.17
Nodes (3): auth_service(), fake_repository(), FakeRepository

### Community 8 - "Logging Module"
Cohesion: 0.20
Nodes (4): JSONFormatter, Structured JSON logging with per-request context.  `setup_logging` installs a JS, Configure the root logger to emit JSON to stdout. Idempotent., setup_logging()

### Community 10 - "Media Feature"
Cohesion: 0.52
Nodes (7): Media Feature Dependencies, Media Feature Exceptions, Media Feature Models, Media Feature Repository, Media Feature Router, Media Feature Schemas, Media Feature Service

### Community 11 - "Token Lifecycle"
Cohesion: 0.70
Nodes (5): Refresh token Redis revocation pattern, Refresh token Redis storage pattern, Refresh token Redis validation pattern, Token logout flow, Token refresh flow

### Community 12 - "Request ID & Logging"
Cohesion: 0.83
Nodes (4): Structured JSON Logging Module, JSON Log Formatter, Request ID Context Variable, Request ID Middleware

### Community 13 - "Settings Configuration"
Cohesion: 0.67
Nodes (3): BaseSettings, get_settings(), Settings

### Community 14 - "Exception Handlers"
Cohesion: 0.50
Nodes (4): AppError base exception class, AppError exception handler, Register exception handlers function, Register exception handlers call

### Community 15 - "Database Initialization"
Cohesion: 0.67
Nodes (4): Database index creation function, Application lifespan manager, MongoDB database connection singleton, Database async iterator dependency

### Community 17 - "Users Feature"
Cohesion: 0.50
Nodes (4): Users Feature Dependencies, Users Feature Exceptions, Users Feature Repository, Users Feature Router

### Community 18 - "Username Generation"
Cohesion: 0.67
Nodes (3): Generate unique username, User registration flow, Random username generator utility

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
- **42 isolated node(s):** `Comments Service (stub)`, `Comments Data Models (stub)`, `Comments API Schemas (stub)`, `Comments Exceptions (stub)`, `Comments API Router (stub)` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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