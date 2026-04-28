---
name: 854-t60-approved-crypto-algorithms
description: Ensure DVRAG uses approved cryptographic algorithms. HS256 for JWT and bcrypt for passwords are currently used — verify key lengths and consider RS256 upgrade.
---

# 854-T60: Use Correct and Approved Cryptographic Algorithms

**Category:** CODE_FIX
**SD Elements:** [854-T60](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current State:**

```python
# app/apis/auth/utils/jwt_auth.py:12-13
ALGORITHM = "HS256"     # HMAC-SHA256 — approved, but symmetric
VERIFY_SIGNATURE = True # MUST remain True
```

```python
# app/apis/auth/utils/utils.py:13
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # approved
```

**Issues to Address:**

1. `JWT_SECRET_KEY` is generated with `secrets.token_hex(32)` = 256-bit key for HS256 — acceptable key length.
2. However, HS256 is a symmetric algorithm — if the key is compromised, all tokens can be forged. Consider RS256 (asymmetric) for production.
3. bcrypt work factor should be >= 12 (passlib default is 12).

**Required Fixes:**

```python
# app/config.py — ensure minimum key length
def _get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        secret = secrets.token_hex(32)  # 256-bit = good for HS256
        warnings.warn(...)
    elif len(secret) < 32:
        raise ValueError("JWT_SECRET_KEY must be at least 32 characters (256 bits)")
    return secret

# app/apis/auth/utils/utils.py — explicitly set bcrypt rounds
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
```

**Success Criteria:**

- JWT uses HS256 with >= 256-bit key (or RS256 with 2048-bit RSA key)
- bcrypt work factor >= 12
- `VERIFY_SIGNATURE = True` enforced

**Status:** Pending
