---
name: 854-t20-generate-unique-session-ids
description: Ensure session IDs (JWT tokens) are unique, non-predictable, and are reset after authentication events. Verify DVRAG JWT implementation is secure.
---

# 854-T20: Generate Unique Session IDs and Reset Old IDs After Authentication

**Category:** CODE_FIX
**SD Elements:** [854-T20](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 9

**Current Code:**

```python
# app/apis/auth/utils/utils.py:117-125
def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

**Issue:** JWT tokens lack a unique identifier (jti claim), making them non-revocable. Additionally, `VERIFY_SIGNATURE = True` in `jwt_auth.py:13` should be kept `True` — confirm it is.

**Required Fix:**

1. Add a `jti` (JWT ID) claim to every token using `secrets.token_hex(16)`.
2. Ensure `VERIFY_SIGNATURE = True` remains in `app/apis/auth/utils/jwt_auth.py`.
3. For logout, implement a token denylist (Redis or database) to invalidate the `jti`.

```python
# app/apis/auth/utils/utils.py - add jti claim
import secrets

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({
        "exp": expire,
        "jti": secrets.token_hex(16),  # unique token ID
        "iat": datetime.now(timezone.utc),
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

**Success Criteria:**

- Every JWT contains a unique `jti` claim
- `VERIFY_SIGNATURE = True` in jwt_auth.py (confirmed, do not change)
- Token expiry is enforced (ACCESS_TOKEN_EXPIRE_MINUTES = 30)

**Status:** Pending
