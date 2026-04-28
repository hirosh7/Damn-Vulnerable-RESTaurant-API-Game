---
name: 854-t35-fine-tune-http-settings
description: Harden HTTP server settings in init_app.py. Add request size limits, improve CORS allowlist from regex to explicit origins, and verify all security headers.
---

# 854-T35: Fine-Tune HTTP Server Settings

**Category:** CODE_FIX
**SD Elements:** [854-T35](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 9

**Current Configuration:**

```python
# app/init_app.py:20-26
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r".*\.(restaurant\.com|deliveryservice\.com)$",  # RISKY REGEX
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)
```

**Issues:**

1. `allow_origin_regex=r".*\."` — the `.*\.` prefix allows `evil.restaurant.com` as well as `legit.restaurant.com`. Use explicit origin list.
2. No request body size limit (default Uvicorn is 4MB — should be lower).
3. HTTP security headers are set (good) but can be strengthened.

**Required Fix:**

```python
# app/init_app.py — tighten CORS configuration
ALLOWED_ORIGINS = [
    "https://restaurant.com",
    "https://www.restaurant.com",
    "https://app.restaurant.com",
    "https://deliveryservice.com",
    "https://www.deliveryservice.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # explicit list, not regex
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],  # remove OPTIONS if not needed
    allow_headers=["Authorization", "Content-Type", "Accept"],
)
```

```python
# Add request size limit middleware
from starlette.middleware.base import BaseHTTPMiddleware

class LimitRequestSizeMiddleware(BaseHTTPMiddleware):
    MAX_BODY_SIZE = 1 * 1024 * 1024  # 1 MB

    async def dispatch(self, request, call_next):
        if request.headers.get("content-length"):
            if int(request.headers["content-length"]) > self.MAX_BODY_SIZE:
                return Response("Request too large", status_code=413)
        return await call_next(request)

app.add_middleware(LimitRequestSizeMiddleware)
```

**Success Criteria:**

- CORS uses explicit origin list, not regex
- Request body size limit of 1 MB enforced
- All existing security headers preserved

**Status:** Pending
