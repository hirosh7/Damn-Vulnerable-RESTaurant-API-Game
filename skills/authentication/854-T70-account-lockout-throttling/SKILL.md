---
name: 854-t70-account-lockout-throttling
description: Implement account lockout for failed login attempts on the /token endpoint. Current implementation has rate limiting but no account-level lockout.
---

# 854-T70: Implement Account Lockout or Authentication Throttling for System Accounts

**Category:** CODE_FIX
**SD Elements:** [854-T70](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current State:**

```python
# app/apis/auth/services/get_token_service.py:18-20
@router.post("/token")
@limiter.limit("10/minute")   # IP-based rate limiting only
async def get_token(request: Request, form_data, db):
```

**Issue:** Only IP-based rate limiting (slowapi). A single IP can try different usernames, or multiple IPs can attack the same account. No account-level lockout is implemented.

**Required Fix:**

Add a failed-attempts counter to the User model and lock accounts after N failures.

```python
# app/db/models.py — add lockout fields
class User(Base):
    # ... existing fields ...
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
```

```python
# app/apis/auth/utils/utils.py — update authenticate_user
def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    # Check if account is locked
    if user.locked_until and datetime.now() < user.locked_until:
        return False
    if not verify_password(password, user.password):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.now() + timedelta(minutes=15)
        db.commit()
        return False
    # Reset on success
    user.failed_login_attempts = 0
    user.locked_until = None
    db.commit()
    return user
```

Also create an Alembic migration for the new columns.

**Success Criteria:**

- Accounts are locked after 5 failed login attempts
- Lockout duration is configurable (default: 15 minutes)
- Alembic migration exists for new columns

**Status:** Pending
