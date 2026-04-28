---
name: 854-t1889-secure-authorization-server-config
description: Harden the OAuth2/JWT authorization server configuration. Review VERIFY_SIGNATURE flag, algorithm allowlist, audience validation, and issuer claim in the FastAPI JWT implementation.
---

# 854-T1889: Secure the Configuration of the Authorization Server

**Category:** CODE_FIX
**SD Elements:** [854-T1889](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Current Configuration:**

```python
# app/apis/auth/utils/jwt_auth.py:11-15
SECRET_KEY = Settings.JWT_SECRET_KEY
ALGORITHM = "HS256"
VERIFY_SIGNATURE = True  # GOOD — do not change

payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM],  # GOOD — algorithm list is restricted
    options={"verify_signature": VERIFY_SIGNATURE},
)
```

**Issues to Address:**

1. No `aud` (audience) claim validation — tokens issued by this server could be replayed at other services.
2. No `iss` (issuer) claim — tokens don't specify their origin.
3. No `nbf` (not-before) claim — tokens are valid immediately, allowing clock-skew attacks.
4. Token revocation is not implemented (see T20 for jti).

**Required Fix:**

```python
# app/apis/auth/utils/utils.py — add security claims
def create_access_token(data: dict, expires_delta=None):
    import secrets
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": secrets.token_hex(16),
        "iss": "dvrag-api",
        "aud": "dvrag-clients",
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# app/apis/auth/utils/jwt_auth.py — validate claims
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM],
    audience="dvrag-clients",
    options={"verify_signature": True, "verify_aud": True, "verify_iss": True},
)
```

**Success Criteria:**

- `VERIFY_SIGNATURE = True` remains enforced
- `iss` and `aud` claims present in all tokens
- Algorithm list restricted to `["HS256"]` (no `none` algorithm allowed)

**Status:** Pending
