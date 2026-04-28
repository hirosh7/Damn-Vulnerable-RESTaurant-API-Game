---
name: 854-t338-control-access-resources
description: Ensure all API endpoints require authentication and proper role-based authorization. Audit all routes in app/apis/router.py for missing auth dependencies.
---

# 854-T338: Control Access to Resources Through User Authentication and Authorization

**Category:** CODE_FIX
**SD Elements:** [854-T338](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Current RBAC Implementation:**

```python
# app/apis/auth/utils/roles_based_auth_checker.py:6-17
class RolesBasedAuthChecker:
    def __init__(self, required_roles):
        self.required_roles = required_roles
    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.required_roles:
            raise HTTPException(status_code=403, detail="Unauthorized")
        return True
```

**Audit Required — Check Each Endpoint:**

1. `/healthcheck` — intentionally public (acceptable)
2. `/token` — public (login endpoint, acceptable)
3. `/reset-password` — public (intentional, rate-limited)
4. `/menu GET` — should verify: is public menu access intended?
5. `/admin/*` — requires CHEF role (verified)
6. `/debug` — requires CHEF role (verified)

**Required Fix:**

1. Ensure all sensitive endpoints (order history, user profiles) require authentication.
2. The `get_orders_service.py` should use `get_current_user` and filter by `current_user.id`.
3. The referrals endpoint should verify `current_user.id` matches request data.

```python
# Verify all protected endpoints have get_current_user or RolesBasedAuthChecker:
from apis.auth.utils import get_current_user, RolesBasedAuthChecker
# Example for orders:
@router.get("/orders/my")
def get_my_orders(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()
```

**Success Criteria:**

- All endpoints requiring authentication have `Depends(get_current_user)` dependency
- No unprotected endpoints return sensitive data
- RBAC enforced consistently

**Status:** Pending
