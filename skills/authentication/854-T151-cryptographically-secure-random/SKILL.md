---
name: 854-t151-cryptographically-secure-random
description: Replace non-cryptographic random.choice() in referrals/utils.py with secrets.choice() or secrets.token_urlsafe(). The referral code generator uses Python's non-secure random module.
---

# 854-T151: Use Cryptographically Secure Random Numbers

**Category:** CODE_FIX
**SD Elements:** [854-T151](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Vulnerable Code:**

```python
# app/apis/referrals/utils.py:1-11
import random
import string

def _generate_code() -> str:
    """Generate an 8-character uppercase alphanumeric code."""
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(8))  # NOT SECURE
```

`random.choice()` uses a Mersenne Twister PRNG which is predictable — an attacker who observes enough referral codes can predict future ones.

**Required Fix:**

```python
# app/apis/referrals/utils.py — use secrets module
import secrets
import string

def _generate_code() -> str:
    """Generate a cryptographically secure 8-character uppercase alphanumeric code."""
    characters = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(characters) for _ in range(8))
```

Or use `secrets.token_urlsafe(8)` for a URL-safe token.

**Note:** `app/apis/auth/utils/text_code_utils.py` already correctly uses `secrets.randbelow()` — do not modify it.

**Success Criteria:**

- `random` module not used for security-sensitive code generation
- `secrets.choice()` or `secrets.token_*` functions used instead
- All security tokens are unpredictable

**Status:** Pending
