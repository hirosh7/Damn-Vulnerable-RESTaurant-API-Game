---
name: 854-t1362-message-throttling-web-apis
description: Extend rate limiting to all sensitive API endpoints. Currently only /token and /reset-password have rate limiting; other endpoints that operate on user data are unprotected.
---

# 854-T1362: Perform Message Throttling in Web APIs

**Category:** CODE_FIX
**SD Elements:** [854-T1362](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current Rate Limiting:**

```python
# app/apis/auth/services/get_token_service.py
@limiter.limit("10/minute")  # GOOD — token endpoint

# app/apis/auth/services/reset_password_service.py
@limiter.limit("5/minute")  # GOOD — reset endpoint
```

**Missing Rate Limiting on:**
- `/orders` POST (order creation) — vulnerable to DoS
- `/menu` PUT (menu item creation) — vulnerable to bulk injection
- `/users/register` — vulnerable to account enumeration/spam

**Required Fix:**

```python
# app/apis/auth/services/register_user_service.py — add rate limit
@router.post("/register")
@limiter.limit("3/minute")  # prevent registration spam
async def register_user(request: Request, ...):
    ...

# app/apis/orders/services/create_order_service.py — add rate limit
@router.post("/orders")
@limiter.limit("10/minute")  # prevent order spam per IP
async def create_order(request: Request, ...):
    ...

# app/apis/menu/services/create_menu_item_service.py — add rate limit
@router.put("/menu")
@limiter.limit("30/minute")
async def create_menu_item(request: Request, ...):
    ...
```

Also add a global default rate limit in `app/init_app.py`:

```python
# app/rate_limiting.py — add default limit
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200/minute"],  # global fallback
)
```

**Success Criteria:**

- `/register` endpoint has rate limiting
- `/orders` POST has rate limiting
- Global fallback rate limit is configured

**Status:** Pending
