---
name: 854-t2599-connection-string-pollution
description: Protect the PostgreSQL connection string from parameter injection. The URL is constructed from environment variables — validate each component.
---

# 854-T2599: Protect Against Connection String Parameter Pollution

**Category:** CODE_FIX
**SD Elements:** [854-T2599](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 9

**Current Code:**

```python
# app/config.py:64-67
@property
def DATABASE_URL(self) -> str:
    if self.DB_BACKEND == "memory":
        return "sqlite://"
    return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
```

**Issue:** If any of the environment variables contain special characters (e.g., `@`, `?`, `#`), the connection string may be misinterpreted. An attacker with control over environment variables could inject additional connection parameters.

**Required Fix:**

Use URL-encoding for user-supplied components, or use SQLAlchemy's `URL.create()`:

```python
# app/config.py — use sqlalchemy URL builder
from sqlalchemy.engine import URL

@property
def DATABASE_URL(self) -> str:
    if self.DB_BACKEND == "memory":
        return "sqlite://"
    return str(URL.create(
        drivername="postgresql",
        username=self.POSTGRES_USER,
        password=self.POSTGRES_PASSWORD,
        host=self.POSTGRES_SERVER,
        port=int(self.POSTGRES_PORT),
        database=self.POSTGRES_DB,
    ))
```

`sqlalchemy.engine.URL.create()` properly escapes all components, preventing parameter injection.

**Success Criteria:**

- `URL.create()` used instead of f-string for DATABASE_URL
- No injection possible via special characters in env vars
- Connection works correctly with safe characters

**Status:** Pending
