---
name: 854-t1390-protect-personal-data
description: Ensure PII (phone numbers, names, addresses) is protected throughout the application lifecycle. The app stores and exposes PII without sufficient safeguards.
---

# 854-T1390: Protect Personal Data

**Category:** CODE_FIX
**SD Elements:** [854-T1390](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**PII Inventory:**

| Field | Location | Protection | Gap |
|-------|----------|-----------|-----|
| `username` | User.username | None | Low risk — usernames are typically public |
| `phone_number` | User.phone_number, Order.phone_number | None | **HIGH — exposed via API** |
| `first_name`, `last_name` | User.first_name/last_name | None | Exposed via API |
| `delivery_address` | Order.delivery_address | None | **HIGH — exposed via order GET** |
| `password` | User.password | bcrypt | GOOD |

**API Exposure Issues:**

```python
# app/apis/auth/schemas.py — UserRead currently includes all PII
class UserRead(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    phone_number: str  # returned in API response
    role: str
```

**Required Fixes:**

1. **API response minimization** — exclude sensitive fields from list endpoints:

```python
# app/apis/auth/schemas.py
class UserReadPublic(BaseModel):
    id: int
    username: str
    role: str
    # No PII fields exposed to other users

class UserReadSelf(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    phone_number: str  # only accessible to account owner
    role: str
```

2. **Phone number masking in responses** for non-owners:

```python
def mask_phone(phone: str) -> str:
    if not phone:
        return ""
    return "***-***-" + phone[-4:]
```

3. **Audit logging** for PII access (see T349).

4. **Field-level access control** — only user can see their own phone number.

**Success Criteria:**

- Other users cannot see another user's phone number or delivery address
- Admin can see but access is logged
- PII responses filtered based on caller identity

**Status:** Pending
