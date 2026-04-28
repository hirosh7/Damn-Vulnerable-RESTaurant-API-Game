---
name: 854-t38-bind-sql-variables
description: Verify all SQL queries use parameterized statements via SQLAlchemy ORM. Confirm no raw SQL string concatenation exists. Related to preventing SQL injection.
---

# 854-T38: Bind Variables in SQL Statements

**Category:** CODE_FIX
**SD Elements:** [854-T38](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 10

**Current State (MOSTLY COMPLIANT):**

The app uses SQLAlchemy ORM which automatically uses parameterized queries:

```python
# SAFE — SQLAlchemy ORM (parameterized)
db.query(User).filter(User.username == username).first()
db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
```

**Audit Required:**

Search for raw SQL usage that might be unsafe:

```bash
# Check for raw SQL in the codebase
grep -rn "execute\|text(\|raw_connection\|cursor" app/ --include="*.py"
```

Also check for f-string or format() in SQL contexts:

```bash
grep -rn "f\"SELECT\|f'SELECT\|% SELECT\|format.*SQL" app/ --include="*.py"
```

**Required Fix:**

If any raw SQL is found, convert to parameterized format:

```python
# WRONG — vulnerable to SQLi
db.execute(f"SELECT * FROM users WHERE username = '{username}'")

# CORRECT — parameterized
from sqlalchemy import text
db.execute(text("SELECT * FROM users WHERE username = :username"), {"username": username})

# OR better — use ORM
db.query(User).filter(User.username == username).first()
```

**Success Criteria:**

- No raw SQL string concatenation with user input
- All queries use SQLAlchemy ORM or parameterized `text()` calls
- `grep` for raw SQL returns no dangerous patterns

**Status:** Pending
