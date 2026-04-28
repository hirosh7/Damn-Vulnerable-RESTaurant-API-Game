---
name: 854-t59-use-standard-crypto-libraries
description: Verify DVRAG uses only standard cryptographic libraries. Confirm passlib/bcrypt and python-jose are used correctly and no custom crypto exists.
---

# 854-T59: Use Standard Libraries for Cryptography

**Category:** CODE_FIX
**SD Elements:** [854-T59](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current State (COMPLIANT):**

```python
# app/apis/auth/utils/utils.py:13
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

```python
# app/apis/auth/utils/jwt_auth.py:7
from jose import JWTError, jwt
ALGORITHM = "HS256"
```

The app uses:
- `passlib` with `bcrypt` for password hashing (standard, approved)
- `python-jose` for JWT (standard, approved)
- No custom cryptographic implementations found

**Verification Tasks:**

1. Confirm no `hashlib.md5()` or `hashlib.sha1()` usage for security purposes.
2. Confirm no custom encryption/decryption functions exist.
3. Verify passlib and python-jose are up to date in `pyproject.toml`.

```bash
# Check for unsafe hash usage
grep -r "md5\|sha1\|DES\|RC4" app/ --include="*.py"
```

**Required Fix:**

- No code changes required if the grep above returns no results for security-critical uses.
- Update pyproject.toml to use latest versions of passlib and python-jose if outdated (cross-reference T186).

**Success Criteria:**

- No custom crypto implementations
- No MD5/SHA1/DES/RC4 used for security purposes
- passlib + bcrypt and python-jose versions are current

**Status:** Pending
