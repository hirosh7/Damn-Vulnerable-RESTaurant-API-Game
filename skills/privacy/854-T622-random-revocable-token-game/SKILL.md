---
name: 854-t622-random-revocable-token-game
description: The referral code system in app/apis/referrals/utils.py uses non-cryptographic random. Codes should be unpredictable and revocable. Cross-reference T151.
---

# 854-T622: Assign a Random Revocable Token to Actions and Achievements in the Game

**Category:** CODE_FIX
**SD Elements:** [854-T622](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Vulnerable Code:**

```python
# app/apis/referrals/utils.py:1-11
import random
import string

def _generate_code() -> str:
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(8))  # NOT CRYPTOGRAPHICALLY SECURE
```

The referral code system uses Python's `random` module which is predictable. Referral codes act as game tokens (they enable discount coupons) and must be cryptographically random.

**Required Fix:**

```python
# app/apis/referrals/utils.py — use secrets module
import secrets
import string

def _generate_code() -> str:
    """Generate a cryptographically secure referral code."""
    characters = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(characters) for _ in range(12))  # 12 chars for higher entropy
```

Additionally, implement revocation:

```python
# app/db/models.py — add revoked field to User
class User(Base):
    referral_code = Column(String, unique=True, index=True, nullable=True)
    referral_code_active = Column(Boolean, default=True, nullable=False)  # revocation flag
```

```python
# app/apis/referrals/utils.py — check revocation
def get_referral_code(db, db_user):
    if db_user.referral_code is None or not db_user.referral_code_active:
        db_user.referral_code = _generate_code()
        db_user.referral_code_active = True
        db.commit()
    return db_user.referral_code
```

**Success Criteria:**

- Referral codes use `secrets.choice()` (see T151)
- Codes are at least 12 characters (72 bits of entropy)
- Code revocation is supported

**Status:** Pending
