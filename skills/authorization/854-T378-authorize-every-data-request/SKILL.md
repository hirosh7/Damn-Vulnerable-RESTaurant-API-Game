---
name: 854-t378-authorize-every-data-request
description: Fix IDOR (Insecure Direct Object Reference) vulnerability in the orders and user profile endpoints. Users can access other users' orders and profiles by guessing IDs.
---

# 854-T378: Authorize Every Request for Data Objects

**Category:** CODE_FIX
**SD Elements:** [854-T378](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Vulnerability (Level 2 — IDOR):**

The vulnerability test in `app/tests/vulns/level_2_unrestricted_profile_update_IDOR.py` confirms:
- Users can update other users' profiles by supplying a different user ID
- Object-level authorization is missing

**Vulnerable Pattern:**

```python
# Any endpoint that fetches by ID without verifying ownership
db.query(Order).filter(Order.id == order_id).first()
# Missing: .filter(Order.user_id == current_user.id)
```

**Required Fix:**

For EVERY endpoint that accesses a data object by ID, add an ownership/role check:

```python
# app/apis/orders/services/get_order_service.py — add ownership check
@router.get("/orders/{order_id}")
def get_order(
    order_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id  # OWNERSHIP CHECK
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
```

```python
# app/apis/auth/services/patch_profile_service.py — fix IDOR
@router.patch("/users/me")
def update_my_profile(
    updates: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],  # use current_user.id
    db: Session = Depends(get_db),
):
    # Only update CURRENT user's profile, never accept user_id from request body
    return update_user(db, current_user.username, updates)
```

**Success Criteria:**

- All object fetch queries filter by `current_user.id` or role check
- No user can access or modify another user's data
- Level 2 IDOR test passes (vulnerability is fixed)

**Status:** Pending
