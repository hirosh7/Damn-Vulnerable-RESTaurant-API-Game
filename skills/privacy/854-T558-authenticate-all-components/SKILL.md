---
name: 854-t558-authenticate-all-components
description: Ensure all inter-component communication is authenticated. The app communicates with PostgreSQL using credentials — verify the connection is authenticated and TLS-secured.
---

# 854-T558: Authenticate All Other Components Before Any Network Communication

**Category:** CODE_FIX
**SD Elements:** [854-T558](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 9

**Current State:**

```python
# app/config.py:64-67
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
```

The application authenticates with PostgreSQL via username/password. However:
- No TLS between app and PostgreSQL
- The default `admin/password` credentials are weak (see T69, T76)

**Required Fix:**

1. Enable TLS for PostgreSQL connections by adding `sslmode=require`:

```python
# app/config.py — add SSL configuration
@property
def DATABASE_URL(self) -> str:
    if self.DB_BACKEND == "memory":
        return "sqlite://"
    from sqlalchemy.engine import URL
    url = URL.create(
        "postgresql",
        username=self.POSTGRES_USER,
        password=self.POSTGRES_PASSWORD,
        host=self.POSTGRES_SERVER,
        port=int(self.POSTGRES_PORT),
        database=self.POSTGRES_DB,
        query={"sslmode": "prefer"},  # use TLS when available
    )
    return str(url)
```

2. For production, use `sslmode=require` with a CA certificate.

3. Ensure the external image fetching (requests.get in menu/utils.py) uses TLS — see T156.

**Success Criteria:**

- PostgreSQL connection uses `sslmode=prefer` (development) or `sslmode=require` (production)
- All external HTTP calls use HTTPS
- Credentials are not hardcoded (see T69, T76)

**Status:** Pending
