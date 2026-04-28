---
name: 854-t49-disable-debug-capabilities
description: Disable or gate the /debug endpoint and ensure it is never accessible in production. Currently any authenticated CHEF user can access full system info, env vars, and memory stats.
---

# 854-T49: Disable and Remove Debug Capabilities and Code/Data

**Category:** CODE_FIX
**SD Elements:** [854-T49](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Vulnerable Code:**

```python
# app/apis/debug/services/get_debug_info_service.py:40-78
@router.get("/debug", status_code=status.HTTP_200_OK)
def get_debug_info_service(current_user, db):
    # Returns: os_info, env_vars (filtered), disk_usage, memory_usage
    return {"os_info": ..., "env_vars": _safe_env(), ...}
```

The `/debug` endpoint is already `include_in_schema=False` in router.py and sensitive env vars are redacted, but it still exposes OS info, memory, and disk stats to any authenticated CHEF.

**Required Fix:**

1. Gate the `/debug` endpoint on the `ENV` setting — disable in production entirely.
2. Move the debug endpoint behind a feature flag.

```python
# app/apis/debug/service.py — add environment gate
from config import ENV, ENVIRONMENT
from fastapi import APIRouter

router = APIRouter()

if ENVIRONMENT != ENV.PRODUCTION:
    from apis.debug.services.get_debug_info_service import router as debug_info_router
    router.include_router(debug_info_router)
```

```python
# app/apis/router.py — already has include_in_schema=False
# Add environment check:
if ENVIRONMENT != ENV.PRODUCTION:
    api_router.include_router(debug_router, prefix="", tags=["debug"], include_in_schema=False)
```

**Success Criteria:**

- `/debug` endpoint returns 404 when `ENV=production`
- No debug endpoint in OpenAPI schema
- Sensitive information not exposed to production users

**Status:** Pending
