---
name: 854-t536-restrict-message-size
description: Add body size limits to all API endpoints to prevent DoS via oversized requests. No request size limits are currently configured in FastAPI/Uvicorn.
---

# 854-T536: Restrict the Size of Incoming Messages in Services

**Category:** CODE_FIX
**SD Elements:** [854-T536](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Issue:**

The FastAPI application accepts arbitrarily large request bodies. An attacker can send enormous payloads to exhaust memory or CPU.

```python
# app/init_app.py — no size limit middleware present
app = FastAPI(...)
# rate limiting is by request count, not size
```

**Required Fix:**

Add a request size limit middleware in `app/init_app.py`:

```python
# app/init_app.py — add size limit middleware
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

MAX_REQUEST_BODY_SIZE = 1 * 1024 * 1024  # 1 MB

class MaxBodySizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_size: int = MAX_REQUEST_BODY_SIZE):
        super().__init__(app)
        self.max_size = max_size

    async def dispatch(self, request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_size:
            return Response(
                content='{"detail":"Request body too large"}',
                status_code=413,
                media_type="application/json",
            )
        return await call_next(request)

app.add_middleware(MaxBodySizeMiddleware)
```

Also configure Uvicorn's `limit_concurrency` in `docker-compose.yml`:

```yaml
command: bash -c "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8091 --workers 1 --limit-max-requests 10000"
```

**Success Criteria:**

- Request bodies > 1 MB return HTTP 413
- Middleware is applied to all routes
- Uvicorn has concurrency limits configured

**Status:** Pending
