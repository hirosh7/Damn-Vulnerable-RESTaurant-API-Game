---
name: 854-t627-secure-transactional-processing
description: Ensure order and coupon transactions are atomic and race-condition-resistant. The create_order_service.py uses db.commit() in multiple places which could allow partial state.
---

# 854-T627: Follow Best Practices for Secure Transactional Processing

**Category:** CODE_FIX
**SD Elements:** [854-T627](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Current Code Issues:**

```python
# app/apis/orders/services/create_order_service.py:46-88
# Multiple db.commit() calls — if one fails, partial state exists
db_order = Order(...)
db.add(db_order)
db.commit()           # COMMIT 1 — order created
db.refresh(db_order)

# ... add items ...
db.commit()           # COMMIT 2 — items added
db.refresh(db_order)

if coupon:
    coupon.used = True
    db.commit()       # COMMIT 3 — coupon marked used
```

**Issue:** Multiple commits create a TOCTOU race condition: if the server crashes between commits, the order exists without items, or items exist without the coupon being marked used (allowing coupon reuse).

**Required Fix:**

Use a single atomic transaction:

```python
# app/apis/orders/services/create_order_service.py — atomic transaction
from sqlalchemy import select
from sqlalchemy.orm import Session

def create_order(order, current_user, db: Session):
    try:
        # Lock coupon with SELECT FOR UPDATE to prevent race condition
        if order.coupon_id:
            coupon = (
                db.execute(
                    select(DiscountCoupon)
                    .filter(DiscountCoupon.id == order.coupon_id)
                    .with_for_update()  # pessimistic locking
                )
                .scalar_one_or_none()
            )
            if not coupon or coupon.used or coupon.user_id != current_user.id:
                raise HTTPException(status_code=400, detail="Invalid or used coupon")

        # All operations in one transaction
        db_order = Order(user_id=current_user.id, ...)
        db.add(db_order)
        db.flush()  # get ID without committing

        for item in order.items:
            db.add(OrderItem(order_id=db_order.id, ...))

        if coupon:
            coupon.used = True
            coupon.used_at = datetime.utcnow()

        db.commit()  # SINGLE COMMIT — atomic
        db.refresh(db_order)
        return db_order
    except Exception:
        db.rollback()
        raise
```

**Success Criteria:**

- All order creation operations in a single atomic transaction
- Coupon usage locked with `SELECT FOR UPDATE`
- No partial state possible on failure

**Status:** Pending
