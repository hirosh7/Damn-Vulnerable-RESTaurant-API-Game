---
name: 854-t2-secure-password-reset
description: Secure the password reset mechanism in the DVRAG FastAPI app. The current implementation sends a reset PIN to the user's phone number but lacks secure token generation, expiry enforcement, and one-time use invalidation.
---

# 854-T2: Secure the Password Reset Mechanism

**Category:** CODE_FIX
**SD Elements:** [854-T2](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 9

**Current Vulnerabilities:**

```python
# app/apis/auth/utils/text_code_utils.py line 12
user.reset_password_code = "".join([str(secrets.randbelow(10)) for _ in range(8)])
user.reset_password_code_expiry_date = datetime.now() + timedelta(minutes=10)
```

The code generates an 8-digit PIN but does not invalidate the code after first use, and the code is stored in plaintext in the database.

**Required Fix:**

1. Hash the reset code before storing it in the database.
2. Invalidate the code immediately after successful use in `app/apis/auth/services/reset_password_new_password_service.py`.
3. Verify expiry before accepting the code.
4. Use `secrets.token_hex(32)` for a higher-entropy token rather than an 8-digit PIN.

```python
# app/apis/auth/utils/text_code_utils.py - secure version
import hashlib, secrets
from datetime import datetime, timedelta

def generate_and_send_code_to_user(user, db):
    raw_token = secrets.token_hex(16)  # 32-char hex token
    user.reset_password_code = hashlib.sha256(raw_token.encode()).hexdigest()
    user.reset_password_code_expiry_date = datetime.now() + timedelta(minutes=10)
    db.add(user)
    db.commit()
    send_code_to_phone_number(user.phone_number, raw_token)
    return True

# In reset_password_new_password_service.py - verify and invalidate
def verify_and_reset(db, username, code, new_password):
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.reset_password_code:
        raise HTTPException(status_code=400, detail="Invalid request")
    if datetime.now() > user.reset_password_code_expiry_date:
        raise HTTPException(status_code=400, detail="Code expired")
    if not secrets.compare_digest(
        hashlib.sha256(code.encode()).hexdigest(),
        user.reset_password_code
    ):
        raise HTTPException(status_code=400, detail="Invalid code")
    # Invalidate immediately
    user.reset_password_code = None
    user.reset_password_code_expiry_date = None
    user.password = get_password_hash(new_password)
    db.commit()
```

**Success Criteria:**

- Reset codes are stored as SHA-256 hashes, not plaintext
- Codes are invalidated after first use
- Expired codes are rejected with appropriate HTTP error
- Token entropy is at least 128 bits

**Status:** Pending
