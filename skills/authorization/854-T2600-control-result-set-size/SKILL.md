---
name: 854-t2600-control-result-set-size
description: Add pagination limits to all list-returning API endpoints to prevent large dataset extraction. Current queries have no LIMIT clause enforced.
---

# 854-T2600: Control the Result Set Size Returned by a Query

**Category:** CODE_FIX
**SD Elements:** [854-T2600](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Issue:**

All list endpoints (menu items, orders, users) return unbounded result sets. An attacker or authorized user could extract the entire dataset:

```python
# app/apis/menu/services/get_menu_service.py
db.query(MenuItem).all()  # No limit — returns ALL items

# app/apis/orders/services/get_orders_service.py
db.query(Order).filter(Order.user_id == user_id).all()  # No pagination
```

**Required Fix:**

Add pagination parameters to all list endpoints:

```python
# app/apis/menu/services/get_menu_service.py — add pagination
@router.get("/menu", response_model=list[schemas.MenuItem])
def get_menu(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(default=50, le=100),  # max 100 items per request
):
    return db.query(MenuItem).offset(skip).limit(limit).all()
```

```python
# app/apis/orders/services/get_orders_service.py — paginate orders
@router.get("/orders")
def get_orders(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(default=20, le=50),
):
    return (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .offset(skip).limit(limit).all()
    )
```

**Success Criteria:**

- All list endpoints have a maximum `limit` parameter
- No query returns more than 100 rows per request
- Pagination parameters (`skip`, `limit`) are documented in OpenAPI

**Status:** Pending
