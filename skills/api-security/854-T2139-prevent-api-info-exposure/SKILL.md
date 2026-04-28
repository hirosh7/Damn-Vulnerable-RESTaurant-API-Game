---
name: 854-t2139-prevent-api-info-exposure
description: Prevent information exposure through APIs. The /debug endpoint exposes OS info and the Level 0 vulnerability exposes server technology details via HTTP headers.
---

# 854-T2139: Prevent Information Exposure Through APIs

**Category:** CODE_FIX
**SD Elements:** [854-T2139](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Vulnerability (Level 0 — Technology Details Exposed via HTTP Header):**

```python
# app/tests/vulns/level_0_technology_details_exposed_via_http_header.py
# Server sends "server: uvicorn" header exposing technology stack
```

**Additional Concerns:**

1. Uvicorn's default `server` response header reveals technology stack.
2. `/debug` endpoint exposes OS version, disk, memory (see T49 for disabling in prod).
3. Error messages may expose internal implementation details.

**Required Fixes:**

```python
# app/init_app.py — remove server technology header
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    response.headers["Content-Security-Policy"] = "default-src 'none'"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Server"] = "Restaurant API"  # obscure server identity
    return response
```

```python
# app/main.py — disable OpenAPI docs in production
if ENVIRONMENT == ENV.PRODUCTION:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:
    # Keep docs for development
    app = FastAPI(...)
```

**Success Criteria:**

- Level 0 vulnerability test no longer passes
- `Server` header does not reveal uvicorn/framework
- API documentation not publicly accessible in production

**Status:** Pending
