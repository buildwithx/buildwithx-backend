"""Structured JSON logging with per-request context.

`setup_logging` installs a JSON formatter on the root logger; `get_logger`
returns module-local loggers. A `request_id` is bound via `ContextVar` so
middleware can attach it to every log emitted during a request without
threading it through call signatures.

Usage
-----

1. Configure once at app startup (e.g. in `app/main.py` lifespan):

       from app.core.logging import setup_logging
       setup_logging(level="INFO")  # call before any logger.info()

2. Get a logger per module — name it after the module:

       from app.core.logging import get_logger
       log = get_logger(__name__)

       log.info("article published", extra={"article_id": "abc123"})
       # -> {"ts":"...","level":"INFO","logger":"app.features.articles.service",
       #     "message":"article published","article_id":"abc123"}

   Anything passed via `extra=` is promoted to a top-level JSON field.

3. Bind a `request_id` in middleware so every log inside the request carries it:

       from app.core.logging import set_request_id, reset_request_id

       @app.middleware("http")
       async def request_id_middleware(request, call_next):
           token = set_request_id(request.headers.get("x-request-id") or uuid4().hex)
           try:
               return await call_next(request)
           finally:
               reset_request_id(token)  # always reset, even on exception

   `ContextVar` is task-local, so concurrent requests don't leak IDs into
   each other.

4. Exceptions: prefer `log.exception("...")` inside an `except` block — the
   traceback is captured automatically under the `exc_info` field.
"""
from __future__ import annotations

import json
import logging
import sys
from contextvars import ContextVar, Token
from datetime import datetime, timezone
from typing import Any

_request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)

# LogRecord attributes set by the logging module itself — anything outside this
# set on a record was passed via `extra=` and should be surfaced in the JSON.
_RESERVED_RECORD_ATTRS = frozenset({
    "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
    "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
    "created", "msecs", "relativeCreated", "thread", "threadName",
    "processName", "process", "message", "asctime", "taskName",
})


def set_request_id(request_id: str | None) -> Token[str | None]:
    return _request_id_var.set(request_id)


def get_request_id() -> str | None:
    return _request_id_var.get()


def reset_request_id(token: Token[str | None]) -> None:
    _request_id_var.reset(token)


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.fromtimestamp(record.created, tz=timezone.utc)
        payload: dict[str, Any] = {
            "ts": ts.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        request_id = _request_id_var.get()
        if request_id is not None:
            payload["request_id"] = request_id

        for key, value in record.__dict__.items():
            if key not in _RESERVED_RECORD_ATTRS and not key.startswith("_"):
                payload[key] = value

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack_info"] = record.stack_info

        return json.dumps(payload, default=str, separators=(",", ":"))


def setup_logging(level: str | int = "INFO") -> None:
    """Configure the root logger to emit JSON to stdout. Idempotent."""
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    # Replace existing handlers so re-invocation (tests, reload) doesn't duplicate output.
    for existing in list(root.handlers):
        root.removeHandler(existing)
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
