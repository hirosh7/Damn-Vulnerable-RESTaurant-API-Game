---
name: 854-t2598-query-level-access-control
description: Implement query-level access control so DB queries automatically filter by user context. Ensure no query can return data outside the current user's scope without explicit role bypass.
---

# 854-T2598: Implement Query-Level Access Control

**Category:** CODE_FIX
**SD Elements:** [854-T2598](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Issue:**

The application uses SQLAlchemy ORM but does not enforce query-level access control. Each service manually (and sometimes incorrectly) filters by user ownership.

**Pattern to Enforce:**

All queries against user-scoped tables (orders, order_items, discount_coupons) MUST include a user filter:

```python
# WRONG — returns all orders
db.query(Order).filter(Order.id == order_id).first()

# CORRECT — scoped to current user
db.query(Order).filter(
    Order.id == order_id,
    Order.user_id == current_user.id
).first()
```

**Audit Checklist:**

- `app/apis/orders/services/get_order_service.py` — verify `user_id` filter
- `app/apis/orders/services/get_orders_service.py` — verify `user_id` filter for customer queries
- `app/apis/orders/services/get_orders_for_delivery_service.py` — verify role-based filter
- `app/apis/referrals/service.py` — verify referral codes scoped to user
- `app/apis/users/services/update_user_role_service.py` — admin-only endpoint, verify CHEF role

**Required Fix:**

Add a helper that returns a base query scoped to the current user:

```python
# app/db/query_helpers.py — new file
from db.models import Order, DiscountCoupon

def user_orders_query(db, user_id: int):
    """Returns a base query for orders scoped to the given user."""
    return db.query(Order).filter(Order.user_id == user_id)

def user_coupons_query(db, user_id: int):
    """Returns a base query for discount coupons scoped to the given user."""
    return db.query(DiscountCoupon).filter(DiscountCoupon.user_id == user_id)
```

**Success Criteria:**

- No query returns cross-user data without CHEF/Employee role check
- Helper functions enforce user scoping
- All services audited and confirmed compliant

**Status:** Pending
