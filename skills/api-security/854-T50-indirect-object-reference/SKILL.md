---
name: 854-t50-indirect-object-reference
description: Prevent IDOR attacks by ensuring all direct object references are scoped to the current user. Related to Level 1 (unrestricted deletion) and Level 2 (IDOR) vulnerabilities.
---

# 854-T50: Use Indirect Object Reference Maps if Accessing Files

**Category:** CODE_FIX
**SD Elements:** [854-T50](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Vulnerability Context:**

- Level 1: `app/tests/vulns/level_1_unrestricted_menu_item_deletion.py` — any authenticated user can delete menu items
- Level 2: `app/tests/vulns/level_2_unrestricted_profile_update_IDOR.py` — users can update other users' profiles

**Vulnerable Pattern:**

```python
# app/apis/menu/services/delete_menu_item_service.py
@router.delete("/menu/{item_id}")
def delete_menu_item(item_id: int, current_user, db):
    # Missing: role check for who can delete
    utils.delete_menu_item(db, item_id)
```

**Required Fixes:**

1. **Menu deletion** — require CHEF or EMPLOYEE role:

```python
# app/apis/menu/services/delete_menu_item_service.py
@router.delete("/menu/{item_id}", status_code=204)
def delete_menu_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    auth=Depends(RolesBasedAuthChecker([UserRole.EMPLOYEE, UserRole.CHEF])),
):
    utils.delete_menu_item(db, item_id)
```

2. **Order access** — scope by `current_user.id` (see T378).

3. **Profile access** — only allow updating `/users/me`, never accept user IDs from request body.

**Success Criteria:**

- Level 1 vulnerability test no longer passes
- Level 2 IDOR vulnerability test no longer passes
- All object-modifying endpoints require role-appropriate authorization

**Status:** Pending
